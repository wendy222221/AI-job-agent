求职规划系统[AI JOB AGENT]
基于大模型Agent架构的智能求职助手，实现从用户能力评估、岗位匹配到简历优化、学习计划生成的全流程自动化服务。

核心功能
JD解析：自动提取岗位关键词、技能要求与职责描述

简历优化：量化评估简历与岗位匹配度，生成针对性优化建议

技能差距分析：对比用户现有技能与岗位要求，识别能力缺口

学习计划生成：根据用户背景自动生成为期6周的个性化学习路径

工具调度：自动调用岗位查询、薪资检索、学习资源推荐等外部工具

技术架构
系统采用分层设计，核心为状态机驱动的Agent决策引擎：

状态机管理：THINKING / EXECUTING / FINALIZING 三状态流转，确保推理链路可控可追溯

工具调度：基于大模型Function Calling机制，实现意图识别与工具的自动化调用

可观测性：全链路Trace日志体系，记录每次推理与工具调用的耗时和Token消耗

用户记忆：跨对话轮次持久化存储用户画像与偏好，增强交互连贯性

交互界面：Streamlit构建的多页面演示环境

快速开始
环境要求
Python 3.9 或更高版本

OpenAI API Key（或其他兼容的大模型API）

安装步骤
克隆仓库

bash
git clone https://github.com/yourusername/job-planning-agent.git
cd job-planning-agent
安装依赖

bash
pip install -r requirements.txt
配置API Key

复制配置模板并填入你的API Key：

bash
cp .env.example .env
编辑 .env 文件：

text
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo
运行应用

bash
streamlit run app.py
项目结构
text
├── agent/                 # Agent核心逻辑
│   ├── state_machine.py   # 状态机实现
│   └── executor.py        # 工具调度器
├── tools/                 # 工具定义
│   ├── job_search.py      # 岗位查询
│   ├── salary_query.py    # 薪资查询
│   └── resource_recommend.py  # 资源推荐
├── memory/                # 用户记忆模块
│   └── user_memory.py
├── modules/               # 业务模块
│   ├── jd_parser.py       # JD解析
│   ├── resume_optimizer.py # 简历优化
│   └── goal_tracker.py    # 学习计划生成
├── utils/                 # 工具函数
│   ├── logger.py          # 日志系统
│   └── token_counter.py   # Token统计
├── app.py                 # Streamlit入口
├── requirements.txt       # 依赖列表
└── .env.example           # 配置模板
使用示例
在界面中输入你的简历文本

粘贴目标岗位的JD链接或内容

系统自动分析并展示匹配度

查看简历优化建议

获取个性化学习计划

技术要点
状态机设计
Agent决策流程被显式划分为三个阶段：

THINKING：分析用户意图，规划执行步骤

EXECUTING：按序调用工具，收集执行结果

FINALIZING：整合结果，生成最终回复

每个状态转换都记录在日志中，便于调试和追溯。

Function Calling 工具调度
工具定义采用标准Schema格式，包含名称、描述和参数定义。大模型根据用户输入自动判断需要调用的工具及其参数。

Trace日志体系
每次Agent执行生成唯一Trace ID，记录：

用户输入

状态转换时间点

每次工具调用的输入输出

Token消耗统计

最终响应内容

未来规划
接入RAG增强JD解析准确率

支持多Agent协作（简历分析Agent + 岗位匹配Agent + 规划Agent）

增加PDF简历解析功能

支持更多大模型提供商（通义千问、文心一言等）

许可证
MIT License


遵循现有的代码风格（PEP 8）。
结果展示<img width="1086" height="765" alt="22a483e1752453e083be4db41c252b98" src="https://github.com/user-attachments/assets/84b1e110-1cea-4eb2-b5ea-d590e05ef220" />
<img width="957" height="699" alt="edf3f66f2978b77d4c89e5e0c134cafb" src="https://github.com/user-attachments/assets/e3edcd09-cddd-457e-8891-8fb38925f8f8" />
<img width="1098" height="819" alt="addd71c08dc2696727de250afa526a80" src="https://github.com/user-attachments/assets/b920b6ed-ef63-47a1-bd45-f45485e78b15" /><img width="1248" height="819" alt="34ee45d067baa43f86daca091782b3f0" src="https://github.com/user-attachments/assets/4ea3de80-2917-4d19-b9ef-e3b3630ede07" />


如果是新功能，请补充相应的文档。

📄 开源协议
本项目基于 MIT 协议开源。

