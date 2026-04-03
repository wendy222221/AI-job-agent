# agents/career_agent.py
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_community.chat_models import ChatZhipuAI


class CareerAgent:
    """职业规划Agent"""

    def __init__(self, api_key, vector_store):
        self.llm = ChatZhipuAI(
            model="glm-4-flash",
            api_key=api_key,
            temperature=0.7
        )
        self.vector_store = vector_store

        # 定义工具
        tools = [
            self.search_jobs_tool,
            self.analyze_skill_gap_tool,
            self.recommend_learning_path_tool,
            self.generate_interview_questions_tool
        ]

        self.agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt="""你是专业的职业规划顾问。你可以：
            1. 搜索相关职位
            2. 分析技能差距
            3. 推荐学习路径
            4. 生成面试问题

            根据用户需求，选择合适的工具提供帮助。
            """
        )

    @tool
    def search_jobs_tool(self, query: str) -> str:
        """搜索相关职位"""
        results = self.vector_store.search_jobs(query)
        if not results:
            return "未找到相关职位"

        output = "找到以下相关职位：\n\n"
        for i, job in enumerate(results[:5], 1):
            output += f"{i}. {job.metadata.get('title', '未知')} - {job.metadata.get('company', '未知')}\n"
            output += f"   内容：{job.page_content[:200]}...\n\n"
        return output

    @tool
    def analyze_skill_gap_tool(self, current_skills: str, target_job: str) -> str:
        """分析技能差距"""
        prompt = f"""
        当前技能：{current_skills}
        目标职位：{target_job}

        请分析技能差距并给出建议：
        1. 现有优势
        2. 需要补充的技能
        3. 学习优先级
        """
        response = self.llm.invoke(prompt)
        return response.content

    @tool
    def recommend_learning_path_tool(self, target_role: str, time_frame: str = "3个月") -> str:
        """推荐学习路径"""
        prompt = f"""
        目标职位：{target_role}
        时间框架：{time_frame}

        请制定详细学习路径：
        1. 分阶段学习目标
        2. 推荐学习资源（课程、书籍、项目）
        3. 每周学习计划
        """
        response = self.llm.invoke(prompt)
        return response.content

    @tool
    def generate_interview_questions_tool(self, job_title: str, company: str = "") -> str:
        """生成面试问题"""
        prompt = f"""
        职位：{job_title}
        公司：{company if company else '科技公司'}

        请生成面试问题：
        1. 技术问题（5个）
        2. 行为问题（5个）
        3. 公司相关的问题（3个）
        4. 反问面试官的问题（3个）
        """
        response = self.llm.invoke(prompt)
        return response.content

    def chat(self, user_input):
        """与用户对话"""
        response = self.agent.invoke({
            "messages": [("human", user_input)]
        })
        return response["messages"][-1].content