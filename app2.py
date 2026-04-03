import streamlit as st
from questionnaire_manager import QuestionnaireManager
from agent_core import CareerAgent
from chains import JDAnalyzerChain, ResumeOptimizerChain
import os
import time

st.set_page_config(page_title="求职助手 - 职业评估", page_icon="🎯", layout="wide")

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'questionnaire' not in st.session_state:
    st.session_state.questionnaire = QuestionnaireManager()

with st.sidebar:
    st.title("🎯 求职助手")
    st.markdown("---")
    steps = ["基本信息", "技能评估", "工作经验", "职业兴趣", "AI 咨询"]
    for i, step in enumerate(steps):
        if i < st.session_state.step:
            st.success(f"✅ {step}")
        elif i == st.session_state.step:
            st.info(f"📌 {step}")
        else:
            st.write(f"⏳ {step}")

st.title("🎯 职业评估问卷")
st.markdown("帮助我们了解你，AI将为你推荐最适合的职业方向")

# ====== 问卷步骤 ======
if st.session_state.step == 0:
    st.session_state.questionnaire.render_section("basic_info")
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("下一步 →", type="primary"):
            ans = st.session_state.questionnaire.get_answers()
            if ans.get("name") and ans.get("age"):
                st.session_state.step = 1
                st.rerun()
            else:
                st.error("请填写姓名和年龄段")

elif st.session_state.step == 1:
    st.session_state.questionnaire.render_section("skills")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← 上一步"):
            st.session_state.step = 0
            st.rerun()
    with col2:
        if st.button("下一步 →", type="primary"):
            ans = st.session_state.questionnaire.get_answers()
            if ans.get("tech_skills"):
                st.session_state.step = 2
                st.rerun()
            else:
                st.warning("请至少选择一项技术技能")

elif st.session_state.step == 2:
    st.session_state.questionnaire.render_section("experience")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← 上一步"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("下一步 →", type="primary"):
            ans = st.session_state.questionnaire.get_answers()
            if ans.get("work_years"):
                st.session_state.step = 3
                st.rerun()
            else:
                st.warning("请选择工作年限")

elif st.session_state.step == 3:
    st.session_state.questionnaire.render_section("interests")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← 上一步"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("完成", type="primary"):
            st.session_state.step = 4
            st.rerun()

# ====== AI 咨询 ======
elif st.session_state.step == 4:
    if 'agent' not in st.session_state:
        st.session_state.agent = CareerAgent()
        st.session_state.agent_running = True
        st.session_state.agent_messages = []
        st.session_state.waiting_for_user = False
        st.session_state.resume_mode = False
        st.session_state.ask_resume = False
        st.session_state.ask_goal = False
        st.session_state.goal_mode = False

    st.title("🤖 AI 职业咨询顾问")
    st.markdown("我已记住你的信息，正在为你智能分析...")

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.agent_messages:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    if msg.get("is_tool"):
                        st.info(msg["content"])
                    else:
                        st.write(msg["content"])

    # ===================== 【修复】输入框永远显示 =====================
    user_input = st.chat_input("输入你的回答...")
    if user_input:
        st.session_state.agent_messages.append({"role": "user", "content": user_input})
        st.session_state.agent.add_to_history("user", user_input)

        # 触发：优化简历
        if ("要" in user_input or "需要" in user_input) and st.session_state.ask_resume and not st.session_state.resume_mode:
            st.session_state.resume_mode = True
            st.rerun()

        # 触发：学习计划
        if ("要" in user_input or "需要" in user_input) and st.session_state.ask_goal and not st.session_state.goal_mode:
            st.session_state.goal_mode = True
            st.rerun()

        st.session_state.waiting_for_user = False
        st.rerun()

    # ===================== 简历优化双窗口 =====================
    if st.session_state.resume_mode:
        st.divider()
        st.subheader("📝 JD 分析 & 简历优化")
        col1, col2 = st.columns(2)
        with col1:
            jd_text = st.text_area("📄 职位描述（JD）", height=260)
        with col2:
            resume_text = st.text_area("✍️ 你的简历内容", height=260)

        if st.button("🚀 一键分析 JD 并优化简历"):
            if jd_text.strip() and resume_text.strip():
                api_key = os.getenv("ZHIPU_API_KEY")
                with st.spinner("正在分析 JD..."):
                    jd_analyzer = JDAnalyzerChain(api_key)
                    jd_result = jd_analyzer.analyze(jd_text)
                with st.spinner("正在优化简历..."):
                    optimizer = ResumeOptimizerChain(api_key)
                    resume_result = optimizer.optimize(resume_text, jd_result)

                st.subheader("📊 JD 分析结果")
                st.success(jd_result)
                st.subheader("✅ 简历优化建议")
                st.success(resume_result)
            else:
                st.warning("请同时输入 JD 和简历内容！")

        if st.button("🔙 返回咨询界面"):
            st.session_state.resume_mode = False
            st.session_state.ask_resume = True
            st.rerun()

    # ===================== Goal Tracker 学习计划 =====================
    elif st.session_state.goal_mode:
        st.divider()
        st.subheader("✅ 求职学习计划（Goal Tracker）")
        user_info = st.session_state.questionnaire.get_answers()

        if st.button("📊 生成 6 周学习计划"):
            with st.spinner("正在生成个性化学习计划..."):
                plan = st.session_state.agent.generate_goal_tracker(user_info)
            st.markdown("## 🎯 6 周求职学习计划")
            st.success(plan)
            st.session_state.agent_messages.append({
                "role": "assistant", "content": f"## 🎯 学习计划\n\n{plan}"
            })

        if st.button("🔙 返回咨询界面"):
            st.session_state.goal_mode = False
            st.rerun()

    # ===================== 报告完成后：问是否优化简历 =====================
    elif not st.session_state.agent_running and not st.session_state.ask_resume:
        st.info("💡 需要我根据你心仪岗位的 JD 帮你优化简历吗？回复：要 / 不要")
        st.session_state.ask_resume = True

    # ===================== 简历优化完成后：问是否生成学习计划 =====================
    elif st.session_state.ask_resume and not st.session_state.goal_mode and not st.session_state.ask_goal:
        st.info("🎯 需要我为你生成 **求职学习计划（Goal Tracker）** 吗？回复：要 / 不要")
        st.session_state.ask_goal = True

    # —— Agent 主逻辑 ——
    if st.session_state.agent_running and not st.session_state.waiting_for_user and not st.session_state.resume_mode and not st.session_state.goal_mode:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.write("🤔 正在智能决策...")
            ans = st.session_state.questionnaire.get_answers()
            dec = st.session_state.agent.think(ans)

            if dec["action"] == "call_tool":
                placeholder.empty()
                st.info(f"🔧 {dec['result']}")
                st.session_state.agent_messages.append({
                    "role": "assistant", "content": dec['result'], "is_tool": True
                })
                st.rerun()

            elif dec["action"] == "ask":
                placeholder.empty()
                q = dec["question"]
                st.write(q)
                st.session_state.agent_messages.append({"role": "assistant", "content": q})
                st.session_state.waiting_for_user = True
                st.rerun()

            elif dec["action"] == "recommend":
                placeholder.write("📝 正在生成最终报告...")
                rep = st.session_state.agent.generate_recommendation(ans)
                placeholder.empty()
                st.markdown("## 🎯 职业规划报告")
                st.write(rep)
                st.session_state.agent_messages.append({
                    "role": "assistant", "content": f"## 🎯 职业规划报告\n\n{rep}"
                })
                st.session_state.agent_running = False
                st.rerun()

    # —— 底部按钮 ——
    if not st.session_state.agent_running and not st.session_state.resume_mode and not st.session_state.goal_mode:
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔄 重新咨询", use_container_width=True):
                st.session_state.agent = CareerAgent()
                st.session_state.agent_running = True
                st.session_state.agent_messages = []
                st.session_state.waiting_for_user = False
                st.session_state.ask_resume = False
                st.session_state.resume_mode = False
                st.session_state.ask_goal = False
                st.session_state.goal_mode = False
                st.rerun()
        with c2:
            if st.button("📝 修改问卷", use_container_width=True):
                st.session_state.step = 0
                st.rerun()
        with c3:
            if st.button("👋 完成", use_container_width=True):
                st.success("祝你求职顺利！")