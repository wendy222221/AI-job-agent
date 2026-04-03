# app.py
import streamlit as st
from chains import JDAnalyzerChain
from chains import ResumeOptimizerChain
from agent import CareerAgent
from utils import JobVectorStore
import json

# 页面配置
st.set_page_config(
    page_title="求职助手",
    page_icon="🎯",
    layout="wide"
)


# 初始化
@st.cache_resource
def init_chains():
    api_key = st.secrets.get("ZHIPU_API_KEY", "")
    if not api_key:
        api_key = st.text_input("请输入智谱AI API Key:", type="password")

    vector_store = JobVectorStore()

    return {
        "jd_analyzer": JDAnalyzerChain(api_key),
        "resume_optimizer": ResumeOptimizerChain(api_key),
        "career_agent": CareerAgent(api_key, vector_store)
    }


# 侧边栏
with st.sidebar:
    st.title("🎯 求职助手")
    st.markdown("---")

    # 功能选择
    function = st.radio(
        "选择功能",
        ["📋 JD分析", "✏️ 简历优化", "🤖 职业规划", "🔍 职位搜索"]
    )

    st.markdown("---")
    st.caption("Powered by Zhipu AI")
    st.caption("v1.0.0")

# 主页面标题
st.title("AI 智能求职助手")
st.markdown("---")

# 初始化 chains（如果需要）
if 'chains' not in st.session_state:
    try:
        st.session_state.chains = init_chains()
    except Exception as e:
        st.error(f"初始化失败: {e}")
        st.stop()

# ==================== 根据侧边栏选择显示不同功能 ====================

# 1. JD分析功能
if function == "📋 JD分析":
    st.header("📋 职位描述分析")
    st.markdown("粘贴职位描述，AI 将为您分析关键要求和技能匹配度")

    # JD 分析界面
    jd_text = st.text_area(
        "职位描述",
        height=300,
        placeholder="请粘贴职位描述...\n\n例如：\n我们正在寻找一位经验丰富的Python开发工程师，负责核心系统开发..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_btn = st.button("🚀 开始分析", type="primary", use_container_width=True)

    if analyze_btn and jd_text:
        with st.spinner("AI 正在分析中..."):
            try:
                # 调用 JD 分析
                result = st.session_state.chains["jd_analyzer"].analyze(jd_text)
                st.success("✅ 分析完成！")

                # 显示结果
                st.subheader("📊 分析结果")
                st.markdown("---")

                # 使用容器美化显示
                with st.container():
                    st.write(result)

            except Exception as e:
                st.error(f"❌ 分析失败: {e}")
                st.info("请检查 API Key 是否正确或稍后重试")
    elif analyze_btn and not jd_text:
        st.warning("⚠️ 请先输入职位描述")

# 2. 简历优化功能
elif function == "✏️ 简历优化":
    st.header("✏️ 简历优化")
    st.markdown("上传或粘贴简历，AI 将根据职位要求为您优化")

    # 创建两列布局
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📄 简历内容")
        # 输入方式选择
        input_method = st.radio("选择输入方式", ["文本粘贴", "文件上传"], horizontal=True, key="resume_input_method")

        resume_text = ""
        uploaded_file = None

        if input_method == "文本粘贴":
            resume_text = st.text_area(
                "简历内容",
                height=300,
                placeholder="请粘贴简历内容...\n\n例如：\n张三\n电话：138****1234\n邮箱：zhangsan@email.com\n\n工作经历：\n2020-2024 某科技公司 Python开发工程师\n- 负责后端API开发\n- 优化数据库查询性能\n\n教育背景：\n2016-2020 某某大学 计算机科学与技术 本科",
                key="resume_text"
            )
        else:
            uploaded_file = st.file_uploader(
                "上传简历文件",
                type=['txt'],
                help="支持 TXT 格式文件",
                key="resume_file"
            )
            if uploaded_file:
                try:
                    resume_text = uploaded_file.read().decode('utf-8')
                    st.success(f"✅ 已上传文件: {uploaded_file.name}")
                except Exception as e:
                    st.error(f"文件读取失败: {e}")

    with col_right:
        st.subheader("🎯 目标职位描述")
        jd_text = st.text_area(
            "职位描述（必填）",
            height=300,
            placeholder="请粘贴目标职位的描述，AI 将根据此要求优化您的简历...\n\n例如：\n职位名称：Python后端开发工程师\n\n岗位职责：\n1. 负责公司核心业务系统的开发\n2. 参与系统架构设计\n\n任职要求：\n1. 3年以上Python开发经验\n2. 熟悉Django/Flask框架\n3. 熟悉MySQL、Redis等数据库",
            help="提供职位描述可以让优化更有针对性"
        )

    # 优化选项
    with st.expander("⚙️ 优化选项"):
        optimize_style = st.selectbox(
            "优化风格",
            ["专业突出", "简洁明了", "成就导向", "技能导向"],
            help="选择简历优化的侧重点"
        )
        st.info("💡 提示：优化后的简历将更匹配目标职位的要求")

    # 优化按钮
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        optimize_btn = st.button("✨ 开始优化", type="primary", use_container_width=True)

    if optimize_btn:
        # 验证输入
        if not resume_text:
            st.warning("⚠️ 请先输入或上传简历内容")
        elif not jd_text:
            st.warning("⚠️ 请先输入目标职位描述")
        else:
            with st.spinner("AI 正在根据职位要求优化简历..."):
                try:
                    # 第一步：分析职位描述
                    st.info("📋 正在分析职位要求...")
                    jd_analysis = st.session_state.chains["jd_analyzer"].analyze(jd_text)

                    # 第二步：根据 JD 分析结果优化简历
                    st.info("✏️ 正在优化简历...")
                    result = st.session_state.chains["resume_optimizer"].optimize(
                        resume_text=resume_text,
                        jd_analysis=jd_analysis
                    )

                    st.success("✅ 优化完成！")

                    # 显示优化结果
                    st.subheader("📝 优化后的简历")
                    st.markdown("---")

                    # 使用容器显示结果
                    with st.container():
                        st.write(result)

                    # 下载按钮
                    st.download_button(
                        label="📥 下载优化后的简历",
                        data=result,
                        file_name="optimized_resume.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                except TypeError as e:
                    # 如果参数名不对，尝试不同的参数格式
                    st.info("尝试使用不同的参数格式...")
                    try:
                        result = st.session_state.chains["resume_optimizer"].optimize(
                            resume_text,
                            jd_text
                        )
                        st.success("✅ 优化完成！")
                        st.write(result)
                    except Exception as e2:
                        st.error(f"❌ 优化失败: {e2}")
                        st.code(f"错误详情: {e2}")
                except Exception as e:
                    st.error(f"❌ 优化失败: {e}")
                    st.info("请检查 API Key 是否正确或稍后重试")

# 3. 职业规划功能
elif function == "🤖 职业规划":
    st.header("🤖 职业规划")
    st.markdown("AI 将根据您的背景和兴趣，提供个性化职业发展建议")

    # 职业规划界面
    with st.form("career_form"):
        col1, col2 = st.columns(2)

        with col1:
            skills = st.text_input("💪 核心技能", placeholder="例如: Python, 数据分析, 项目管理, 团队管理")
            experience = st.number_input("📅 工作经验（年）", min_value=0, max_value=50, value=0, step=1)

        with col2:
            interests = st.text_input("🎯 职业兴趣方向", placeholder="例如: AI工程师, 技术专家, 产品经理, 技术总监")
            education = st.selectbox("🎓 学历背景", ["大专", "本科", "硕士", "博士", "其他"])

        goals = st.text_area("🚀 职业目标",
                             placeholder="描述您的职业目标和期望...\n\n例如：\n- 3年内成为技术专家\n- 希望转向管理岗位\n- 想创业或成为自由职业者",
                             height=100)

        submitted = st.form_submit_button("获取职业规划建议", type="primary", use_container_width=True)

    if submitted:
        if skills or interests:
            with st.spinner("AI 正在分析您的职业规划..."):
                try:
                    # 构建用户信息
                    user_info = {
                        "skills": skills,
                        "experience": experience,
                        "interests": interests,
                        "education": education,
                        "goals": goals
                    }
                    # 调用职业规划
                    result = st.session_state.chains["career_agent"].plan(user_info)
                    st.success("✅ 规划完成！")

                    # 显示结果
                    st.subheader("📋 职业规划建议")
                    st.markdown("---")
                    st.write(result)

                except Exception as e:
                    st.error(f"❌ 规划失败: {e}")
        else:
            st.warning("⚠️ 请至少填写技能或职业兴趣")

# 4. 职位搜索功能
elif function == "🔍 职位搜索":
    st.header("🔍 职位搜索")
    st.markdown("搜索相关职位，AI 将为您匹配最适合的岗位")

    # 职位搜索界面
    col1, col2 = st.columns([3, 1])

    with col1:
        search_keyword = st.text_input("🔎 职位关键词", placeholder="例如: Python开发工程师, 数据分析师, 产品经理")

    with col2:
        location = st.text_input("📍 工作地点", placeholder="例如: 北京, 上海, 深圳, 远程")

    job_type = st.multiselect(
        "📌 职位类型",
        ["全职", "兼职", "实习", "远程"],
        default=["全职"]
    )

    # 高级选项
    with st.expander("🔧 高级筛选"):
        salary_range = st.select_slider(
            "期望薪资范围（K/月）",
            options=["不限", "10-20", "20-30", "30-40", "40-50", "50+"],
            value="不限"
        )
        experience_required = st.selectbox(
            "要求工作经验",
            ["不限", "应届生", "1-3年", "3-5年", "5-10年", "10年以上"]
        )

    col1, col2 = st.columns([1, 4])
    with col1:
        search_btn = st.button("🔍 搜索职位", type="primary", use_container_width=True)

    if search_btn and search_keyword:
        with st.spinner("正在搜索匹配职位..."):
            try:
                # 调用职位搜索
                jobs = st.session_state.chains["career_agent"].search_jobs(
                    keyword=search_keyword,
                    location=location,
                    job_type=job_type
                )

                if jobs:
                    st.success(f"✅ 找到 {len(jobs)} 个相关职位")
                    st.markdown("---")

                    # 显示搜索结果
                    for idx, job in enumerate(jobs, 1):
                        with st.expander(f"📌 {idx}. {job.get('title', '职位名称')} - {job.get('company', '公司名称')}",
                                         expanded=False):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**📍 地点:** {job.get('location', '未指定')}")
                                st.write(f"**📌 类型:** {job.get('type', '未指定')}")
                            with col2:
                                st.write(f"**💰 薪资:** {job.get('salary', '面议')}")
                                st.write(f"**🎯 匹配度:** {job.get('match_score', 'N/A')}")

                            st.write(f"**📝 职位描述:**")
                            st.write(job.get('description', '无描述'))

                            if job.get('requirements'):
                                st.write(f"**✨ 任职要求:**")
                                st.write(job.get('requirements'))
                else:
                    st.info("📭 未找到匹配的职位，请尝试不同的关键词或筛选条件")

            except Exception as e:
                st.error(f"❌ 搜索失败: {e}")
                st.info("职位搜索功能可能需要配置向量数据库，请先确保已正确配置")
    elif search_btn and not search_keyword:
        st.warning("⚠️ 请输入职位关键词进行搜索")

# 页脚
st.markdown("---")
st.markdown("💡 **提示**: AI 分析可能需要几秒钟时间，请耐心等待")
st.markdown("📧 如有问题，请检查 API Key 是否正确配置")