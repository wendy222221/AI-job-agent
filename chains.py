from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatZhipuAI


# ---------------------- JD分析链 ----------------------
class JDAnalyzerChain:
    def __init__(self, api_key):
        self.llm = ChatZhipuAI(
            model="glm-4-flash",
            api_key=api_key,
            temperature=0.1
        )

        self.prompt = PromptTemplate(
            input_variables=["jd_text"],
            template="""
你是专业的招聘专家，请分析以下职位描述（JD）。

JD内容：
{jd_text}

请详细分析：
1. 职位核心要求
2. 必须技能
3. 加分项
4. 工作内容
5. 对应聘者的建议

输出清晰、结构化的分析结果。
"""
        )

        self.chain = self.prompt | self.llm

    def analyze(self, jd_text):
        response = self.chain.invoke({"jd_text": jd_text})
        return response.content


# ---------------------- 简历优化链 ----------------------
class ResumeOptimizerChain:
    def __init__(self, api_key):
        self.llm = ChatZhipuAI(
            model="glm-4-flash",
            api_key=api_key,
            temperature=0.5
        )

        self.prompt = PromptTemplate(
            input_variables=["resume_text", "jd_analysis"],
            template="""
你是专业的简历优化顾问。请根据JD分析结果优化简历。

原始简历：
{resume_text}

JD分析结果：
{jd_analysis}

请进行以下优化：
1. 个人简介优化
2. 工作经历优化（STAR法则+量化）
3. 技能清单优化
4. 整体建议

输出优化后的简历要点。
"""
        )

        self.chain = self.prompt | self.llm

    def optimize(self, resume_text, jd_analysis):
        response = self.chain.invoke({
            "resume_text": resume_text,
            "jd_analysis": jd_analysis
        })
        return response.content