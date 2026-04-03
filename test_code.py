from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 定义工具
@tool
def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"{city}的天气是晴天"

@tool
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 创建模型
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 创建代理
tools = [get_weather, get_current_time]
agent = create_agent(model=llm, tools=tools)

# 使用代理
result = agent.invoke({"messages": [("human", "北京天气怎么样？")]})
print(result)