# chains/jd_analyzer.py
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatZhipuAI


class JDAnalyzerChain:
    """JD分析链"""

    def __init__(self, api_key):
        self.llm = ChatZhipuAI(
            model="glm-4-flash",
            api_key=api_key,
            temperature=0.3
        )

        self.prompt = PromptTemplate(
            input_variables=["jd_text"],
            template="""
            你是一个专业的招聘专家。请分析以下职位描述(JD)，并提取关键信息：

            JD内容：
            {jd_text}

            请按以下格式输出分析结果：

            ## 核心要求
            - 必备技能：
            - 加分技能：
            - 经验要求：
            - 学历要求：

            ## 职责分析
            - 主要职责：
            - 工作重点：

            ## 薪资范围
            - 预估薪资：

            ## 简历匹配建议
            - 需要突出的经验：
            - 需要补充的技能：
            - 简历优化方向：

            ## 面试准备重点
            - 技术问题预测：
            - 行为面试重点：
            """
        )

        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt
        )

    def analyze(self, jd_text):
        """分析JD"""
        return self.chain.run(jd_text=jd_text)