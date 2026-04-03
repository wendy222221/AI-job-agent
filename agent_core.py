import json
import requests
import os
import time
import uuid
from typing import Dict, List, Any, Optional


class AgentState:
    THINKING = "thinking"
    EXECUTING = "executing_tool"
    FINALIZING = "finalizing"
    COMPLETED = "completed"
    FAILED = "failed"


class CareerAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.conversation_history = []
        self.tool_results = []
        self.max_steps = 5
        self.current_step = 0
        self.available_tools = self._get_tools_schema()

        # ===================== 生产级增强（你简历亮点） =====================
        self.trace_id = str(uuid.uuid4())        # 全链路追踪
        self.state = AgentState.THINKING         # 状态机
        self.token_budget = 25000                # token 预算
        self.used_tokens = 0                     # 已用 token
        self.user_memory = {}                    # 长期记忆

    # ===================== 结构化日志 =====================
    def log(self, message, **kwargs):
        log_obj = {
            "trace_id": self.trace_id,
            "step": self.current_step,
            "state": self.state,
            "time": time.time(),
            "message": message,
            **kwargs
        }
        print(json.dumps(log_obj, ensure_ascii=False))

    # ===================== 长期记忆 =====================
    def remember(self, key: str, value: Any):
        self.user_memory[key] = value
        self.log("memory_updated", key=key)

    def recall(self, key: str):
        return self.user_memory.get(key)

    # ===================== 预算 & 终止策略 =====================
    def near_budget(self):
        return self.used_tokens >= self.token_budget * 0.85

    def should_stop(self):
        return self.current_step >= self.max_steps or self.used_tokens >= self.token_budget

    def _get_tools_schema(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_jobs",
                    "description": "根据技能和地点搜索招聘岗位",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "skills": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "技能列表"
                            },
                            "location": {
                                "type": "string",
                                "description": "工作地点"
                            }
                        },
                        "required": ["skills"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_skill_gap",
                    "description": "分析技能与目标岗位差距",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "current_skills": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "当前技能"
                            },
                            "target_job": {
                                "type": "string",
                                "description": "目标岗位"
                            }
                        },
                        "required": ["current_skills", "target_job"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_salary_data",
                    "description": "查询岗位薪资",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市"
                            },
                            "job_title": {
                                "type": "string",
                                "description": "岗位名称"
                            }
                        },
                        "required": ["city", "job_title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_training_resources",
                    "description": "获取学习资源推荐",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "skill": {
                                "type": "string",
                                "description": "技能名称"
                            }
                        },
                        "required": ["skill"]
                    }
                }
            }
        ]

    def _call_llm(self, sys_prompt, user_msg, force_tool=False):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "glm-4-flash",
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_msg}
            ],
            "temperature": 0.1,
            "tools": self.available_tools,
            "tool_choice": "auto" if not force_tool else "none"
        }

        try:
            resp = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            self.used_tokens += 500  # 模拟估算
            return resp.json()["choices"][0]["message"]
        except Exception as e:
            self.log("llm_error", error=str(e))
            return {"content": "", "tool_calls": None}

    def execute_tool(self, tool_name, args):
        self.state = AgentState.EXECUTING
        self.log("executing_tool", tool=tool_name, args=args)

        if tool_name == "search_jobs":
            return self._search_jobs(args.get("skills", []), args.get("location", "全国"))
        elif tool_name == "analyze_skill_gap":
            return self._analyze_skill_gap(args.get("current_skills", []), args.get("target_job", ""))
        elif tool_name == "get_salary_data":
            return self._get_salary_data(args.get("city", ""), args.get("job_title", ""))
        elif tool_name == "get_training_resources":
            return self._get_training_resources(args.get("skill", ""))
        return "未知工具"

    def _search_jobs(self, skills, location="全国"):
        mock = {
            "前端": [{"title": "前端开发工程师", "company": "字节跳动", "salary": "25-40K", "location": location}],
            "后端": [{"title": "后端开发工程师", "company": "阿里", "salary": "28-45K", "location": location}],
            "全栈": [{"title": "全栈开发工程师", "company": "京东", "salary": "28-48K", "location": location}],
            "AI Agent": [{"title": "AI Agent 应用开发", "company": "AI企业", "salary": "30-50K", "location": location}]
        }
        for s in skills:
            for k in mock:
                if k in s or s in k:
                    res = f"📍 {location} 相关岗位推荐：\n"
                    for j in mock[k][:3]:
                        res += f"- {j['title']} @ {j['company']} | {j['salary']}\n"
                    return res
        return "未找到匹配岗位，默认推荐：AI Agent 应用开发 30-50K"

    def _analyze_skill_gap(self, current_skills, target_job):
        standard = {
            "前端开发工程师": ["React", "Vue", "TypeScript", "打包优化"],
            "全栈开发工程师": ["React", "Node.js", "MySQL", "Docker"],
            "AI Agent 应用开发": ["Python", "LLM", "RAG", "Streamlit", "LangChain"]
        }
        req = standard.get(target_job, [])
        missing = [r for r in req if r.lower() not in [c.lower() for c in current_skills]]
        if missing:
            return f"🎯 目标岗位：{target_job}\n📉 技能差距：{', '.join(missing)}"
        else:
            return f"🎯 目标岗位：{target_job}\n✅ 技能基本匹配！"

    def _get_salary_data(self, city, job_title):
        salary_map = {
            "北京": {"前端": "25-40K", "全栈": "30-50K", "后端": "28-45K", "AI Agent": "30-50K"},
            "上海": {"前端": "24-38K", "全栈": "28-48K", "后端": "26-43K", "AI Agent": "29-48K"},
            "深圳": {"前端": "23-36K", "全栈": "27-45K", "后端": "25-42K", "AI Agent": "28-45K"},
            "杭州": {"前端": "20-32K", "全栈": "24-40K", "后端": "22-38K", "AI Agent": "25-40K"},
            "成都": {"前端": "18-28K", "全栈": "20-32K", "后端": "19-30K", "AI Agent": "23-38K"}
        }
        city = city.replace("市", "")
        if city not in salary_map:
            return f"💰 {city} {job_title} 薪资约 20-35K"
        jk = "AI Agent" if "AI Agent" in job_title else "前端" if "前端" in job_title else "全栈" if "全栈" in job_title else "后端"
        return f"💰 {city} {job_title} 平均薪资：{salary_map[city][jk]}"

    def _get_training_resources(self, skill):
        rec = {
            "React": "React官方文档 + B站尚硅谷",
            "Vue": "Vue官方文档 + VueMastery",
            "TypeScript": "TS官方文档 + 深入浅出TypeScript",
            "Node.js": "Node官方文档 + Egg.js教程",
            "Python": "廖雪峰Python + LeetCode刷题",
            "AI Agent": "LangChain官方文档 + RAG实战 + Streamlit项目"
        }
        for k in rec:
            if k.lower() in skill.lower():
                return f"📚 学习 {skill}：{rec[k]}"
        return f"📚 学习 {skill}：官方文档 + 项目实战 + 面试题"

    def think(self, user_answers: Dict) -> Dict:
        self.current_step += 1
        self.state = AgentState.THINKING
        self.log("agent_start_think", user=user_answers)

        # 接近预算自动收尾
        if self.near_budget():
            self.state = AgentState.FINALIZING
            self.log("near_token_budget_auto_finalize")
            return {"action": "recommend"}

        info = user_answers.copy()
        for msg in self.conversation_history:
            if msg["role"] == "user":
                c = msg["content"]
                if "成都" in c: info["city"] = "成都"
                if "北京" in c: info["city"] = "北京"
                if "上海" in c: info["city"] = "上海"
                if "深圳" in c: info["city"] = "深圳"
                if "杭州" in c: info["city"] = "杭州"
                if "agent" in c.lower() or "ai" in c.lower():
                    info["target_job"] = "AI Agent 应用开发"

        info_str = json.dumps(info, ensure_ascii=False, indent=2)
        history_str = json.dumps(self.conversation_history[-5:], ensure_ascii=False, indent=2)
        tools_str = json.dumps(self.tool_results[-5:], ensure_ascii=False, indent=2)

        sys_prompt = """
你是职业规划AI，必须严格输出JSON，不要多余内容。

规则：
1. 必须检查用户信息：技能、目标岗位、城市、工作年限
2. 如果已经提供 → 直接 recommend
3. 如果缺少 → 只问缺失的那一项
4. 需要数据 → call_tool

输出格式只能是：
{"action":"ask","question":"..."}
{"action":"call_tool"}
{"action":"recommend"}
"""

        user_msg = f"""
用户信息：{info_str}
对话历史：{history_str}
工具结果：{tools_str}

请严格输出JSON：
"""

        resp = self._call_llm(sys_prompt, user_msg)
        if resp.get("tool_calls"):
            tool = resp["tool_calls"][0]
            name = tool["function"]["name"]
            args = json.loads(tool["function"]["arguments"])
            res = self.execute_tool(name, args)
            self.tool_results.append({"tool": name, "result": res})
            self.log("tool_success", tool=name)
            return {"action": "call_tool", "tool": name, "result": res}

        content = resp.get("content", "")
        try:
            return json.loads(content)
        except:
            if info.get("target_job") and info.get("city"):
                return {"action": "recommend"}
            missing = []
            if not info.get("target_job"): missing.append("目标岗位")
            if not info.get("city"): missing.append("期望城市")
            return {"action": "ask", "question": f"可以告诉我你的{', '.join(missing)}吗？"}

    def generate_recommendation(self, user_answers):
        self.state = AgentState.COMPLETED
        self.log("generating_final_report")

        sys = """你是资深职业规划师，生成完整、专业、可执行的报告。
包含：
1. 综合评估
2. 推荐岗位（3个）
3. 薪资范围
4. 技能差距
5. 学习路线
6. 求职建议
"""
        msg = f"用户信息：{json.dumps(user_answers)}\n工具数据：{json.dumps(self.tool_results)}"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": "glm-4-flash", "messages": [{"role": "system", "content": sys}, {"role": "user", "content": msg}], "temperature": 0.7}
        try:
            return requests.post(self.api_url, headers=headers, json=payload).json()["choices"][0]["message"]["content"]
        except:
            return "生成报告失败"

    # ===================== 你要的：Goal Tracker 求职计划 =====================
    def generate_goal_tracker(self, user_info):
        self.log("generating_goal_tracker")
        sys_prompt = """
你是求职教练，根据用户目标岗位、技能、城市，生成一份 6 周求职学习计划（Goal Tracker）。
结构：
- 整体目标
- 每周任务
- 技能提升重点
- 投递计划
- 复盘建议
"""
        user_msg = json.dumps(user_info, ensure_ascii=False)
        res = self._call_llm(sys_prompt, user_msg, force_tool=True)
        return res.get("content", "生成计划失败")

    def add_to_history(self, role, content):
        self.conversation_history.append({"role": role, "content": content})

    def reset(self):
        self.conversation_history = []
        self.tool_results = []
        self.current_step = 0
        self.log("agent_reset")


# ===================== 自动化测试集（简历亮点） =====================
if __name__ == "__main__":
    agent = CareerAgent()
    TEST_CASES = [
        {"city": "成都", "target_job": "AI Agent 应用开发", "current_skills": ["Python"]},
        {"city": "北京", "target_job": "前端开发工程师", "current_skills": ["HTML", "CSS"]},
    ]
    for i, case in enumerate(TEST_CASES):
        print(f"\n===== 测试用例 {i+1} =====")
        res = agent.think(case)
        print(res)