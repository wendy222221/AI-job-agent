# questionnaire_manager.py
import streamlit as st
from questionnaire_data import QUESTIONNAIRE


class QuestionnaireManager:
    """管理问卷的类"""

    def __init__(self):
        self.questions = QUESTIONNAIRE
        self.answers = {}

    def render_question(self, question):
        """根据问题类型渲染输入组件"""
        q_id = question["id"]
        q_text = question["question"]

        if question["type"] == "text":
            return st.text_input(
                q_text,
                key=f"q_{q_id}",
                placeholder=question.get("placeholder", "")
            )

        elif question["type"] == "textarea":
            return st.text_area(
                q_text,
                key=f"q_{q_id}",
                placeholder=question.get("placeholder", ""),
                height=question.get("rows", 100)
            )

        elif question["type"] == "select":
            return st.selectbox(
                q_text,
                options=question["options"],
                key=f"q_{q_id}"
            )

        elif question["type"] == "multiselect":
            return st.multiselect(
                q_text,
                options=question["options"],
                key=f"q_{q_id}"
            )

        return None

    def render_section(self, section_key):
        """渲染整个章节"""
        section = self.questions[section_key]
        st.subheader(section["title"])
        st.markdown("---")

        for question in section["questions"]:
            answer = self.render_question(question)
            if answer is not None and answer != []:  # 空列表不算
                self.answers[question["id"]] = answer
            elif answer == []:
                # 多选为空时，跳过
                pass
            elif answer is None:
                pass

        st.markdown("")

    def get_answers(self):
        """获取所有答案"""
        return self.answers