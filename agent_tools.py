# agent_tools.py - Agent 工具集

import requests
import json


class AgentTools:
    """Agent 可调用的工具"""

    @staticmethod
    def search_jobs(skills, location="全国"):
        """搜索招聘岗位"""
        # 这里可以接入真实 API，比如拉勾、Boss直聘
        # 现在先返回模拟数据
        mock_jobs = [
            {
                "title": "前端开发工程师",
                "company": "某互联网公司",
                "location": location,
                "skills": ["React", "Vue", "TypeScript"],
                "salary": "20-35K"
            },
            {
                "title": "全栈开发工程师",
                "company": "某科技公司",
                "location": location,
                "skills": ["React", "Node.js", "Python"],
                "salary": "25-40K"
            }
        ]
        return mock_jobs

    @staticmethod
    def analyze_skill_gap(current_skills, target_job):
        """分析技能差距"""
        # 这里可以调用 AI 做技能匹配
        prompt = f"""
        用户当前技能：{current_skills}
        目标岗位要求：{target_job}
        请列出需要提升的技能和优先级。
        """
        # 调用 LLM 分析...
        return "需要提升：TypeScript、Next.js、性能优化"

    @staticmethod
    def get_salary_data(city, job_title):
        """查询薪资数据"""
        # 可以接入真实薪资 API
        mock_salary = {
            "beijing": {"frontend": "25-40K", "fullstack": "30-50K"},
            "shanghai": {"frontend": "22-38K", "fullstack": "28-48K"},
            "shenzhen": {"frontend": "20-35K", "fullstack": "25-45K"}
        }
        city_key = city.lower()
        job_key = "frontend" if "前端" in job_title else "fullstack"
        return mock_salary.get(city_key, {}).get(job_key, "面议")