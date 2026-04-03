# questionnaire_data.py
"""
职业评估问卷数据
"""

QUESTIONNAIRE = {
    "basic_info": {
        "title": "基本信息",
        "questions": [
            {
                "id": "name",
                "question": "你的姓名（或称呼）？",
                "type": "text",
                "required": True
            },
            {
                "id": "age",
                "question": "你的年龄段？",
                "type": "select",
                "options": ["20-25岁", "26-30岁", "31-35岁", "36-40岁", "40岁以上"],
                "required": True
            },
            {
                "id": "education",
                "question": "你的最高学历？",
                "type": "select",
                "options": ["大专", "本科", "硕士", "博士", "其他"],
                "required": True
            },
            {
                "id": "major",
                "question": "你的专业是什么？",
                "type": "text",
                "placeholder": "例如：计算机科学与技术、工商管理...",
                "required": True
            }
        ]
    },

    "skills": {
        "title": "技能评估",
        "questions": [
            {
                "id": "tech_skills",
                "question": "你掌握哪些技术技能？（可多选）",
                "type": "multiselect",
                "options": [
                    "Python", "Java", "JavaScript", "C++", "Go",
                    "React", "Vue", "Angular",
                    "SQL", "MongoDB", "Redis",
                    "Docker", "Kubernetes",
                    "数据分析", "机器学习", "深度学习",
                    "项目管理", "产品设计"
                ],
                "required": True
            },
            {
                "id": "soft_skills",
                "question": "你的软技能优势？（可多选）",
                "type": "multiselect",
                "options": [
                    "沟通能力", "团队协作", "问题解决", "学习能力",
                    "领导力", "抗压能力", "时间管理"
                ]
            }
        ]
    },

    "experience": {
        "title": "工作经验",
        "questions": [
            {
                "id": "work_years",
                "question": "你的工作年限？",
                "type": "select",
                "options": ["应届生/无经验", "1-3年", "3-5年", "5-8年", "8年以上"],
                "required": True
            },
            {
                "id": "job_roles",
                "question": "你担任过哪些职位？",
                "type": "text",
                "placeholder": "例如：Python开发工程师、产品经理...",
                "required": True
            },
            {
                "id": "projects",
                "question": "请描述你最自豪的项目或成就",
                "type": "textarea",
                "placeholder": "例如：主导开发了日活10万+的电商系统...",
                "rows": 3
            }
        ]
    },

    "interests": {
        "title": "职业兴趣",
        "questions": [
            {
                "id": "work_style",
                "question": "你更喜欢什么样的工作方式？",
                "type": "select",
                "options": [
                    "独立工作，专注技术",
                    "团队协作，共同完成",
                    "管理协调，领导团队"
                ],
                "required": True
            },
            {
                "id": "career_goals",
                "question": "你未来3-5年的职业目标是什么？",
                "type": "textarea",
                "placeholder": "例如：成为技术专家、转向管理岗位...",
                "rows": 2
            },
            {
                "id": "location",
                "question": "期望的工作地点？",
                "type": "text",
                "placeholder": "例如：北京、上海、深圳、远程",
                "required": True
            }
        ]
    }
}