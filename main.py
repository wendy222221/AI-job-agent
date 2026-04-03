import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 加载环境变量（可选）
load_dotenv()

# 1. LLM 大脑
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key="你的API_KEY",  # 替换为你的真实 API key
    base_url="https://api.chatanywhere.tech/v1"
)


# 2. 定义求职工具（使用 @tool 装饰器）
@tool
def analyze_resume(resume_text: str) -> str:
    """分析简历，提取个人优势、技能、经历，指出问题"""
    # 这里可以调用真实的 AI 分析逻辑
    return f"""【简历分析】
简历内容：{resume_text}

分析结果：
✅ 核心优势：沟通能力强、技术扎实
✅ 关键技能：Python、数据分析、项目管理
⚠️ 改进建议：项目经验描述不够量化，建议增加具体数据支撑
📊 匹配度评分：75/100"""


@tool
def match_job(resume_text: str, job_desc: str) -> str:
    """根据岗位JD自动优化简历，生成适配版"""
    return f"""【岗位匹配完成】
原始简历摘要：{resume_text[:100]}...
目标岗位要求：{job_desc[:100]}...

优化建议：
1. 简历中增加与岗位匹配的关键词：数据分析、团队协作
2. 突出相关项目经验
3. 优化工作经历描述，更符合岗位要求

优化后通过率预计提升 40%"""


@tool
def mock_interview(question: str) -> str:
    """模拟面试问答"""
    return f"""【面试回答】
问题：{question}

回答要点：
1. 首先简明扼要地回答问题核心
2. 用具体案例说明（STAR法则）
3. 突出个人优势和价值
4. 适当反问展示思考深度

示例回答：
"这个问题很好，我认为... 以我之前在XX项目中的经验为例... 最终取得了XX成果..." """


# 包装工具列表
tools = [analyze_resume, match_job, mock_interview]

# 3. 创建 Agent（使用新版本 API）
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""你是专业求职顾问AI Agent，擅长：
1. 简历分析：深入分析简历，找出优势和短板
2. 岗位匹配：根据职位描述优化简历
3. 面试辅导：提供专业的面试回答建议
4. 求职规划：制定个性化的求职策略

请根据用户的问题，选择合适的工具提供帮助，回答要专业、实用、有针对性。"""
)


# 4. 使用 Agent（处理用户输入）
def run_agent():
    print("=" * 50)
    print("求职 AI Agent 已启动")
    print("支持功能：简历分析、岗位匹配、面试辅导")
    print("输入 'exit' 或 'quit' 退出")
    print("=" * 50)

    while True:
        user_input = input("\n你：").strip()
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("感谢使用，祝求职顺利！")
            break

        if not user_input:
            continue

        try:
            # 调用 agent
            response = agent.invoke({
                "messages": [("human", user_input)]
            })

            # 提取并打印回复
            if "messages" in response and response["messages"]:
                last_message = response["messages"][-1]
                if hasattr(last_message, 'content'):
                    print("\n=== Agent 回复 ===")
                    print(last_message.content)
                else:
                    print("\n=== Agent 回复 ===")
                    print(last_message)
            else:
                print("\n=== Agent 回复 ===")
                print(response)

        except Exception as e:
            print(f"\n错误：{e}")
            print("请检查 API key 和网络连接")


# 5. 运行
if __name__ == "__main__":
    run_agent()