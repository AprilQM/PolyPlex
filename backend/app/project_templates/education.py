"""
教育领域页面模板 - 课程大纲、教案设计、学生进度、评估评分、知识图谱、课堂活动
"""
from app.page_components import (
    PageTemplate,
    TextBlockComponent, TableComponent, StepsComponent, ListComponent,
    MindmapComponent, MetricCardComponent, ProgressBarComponent, ScorecardComponent,
    DividerComponent, SpacerComponent,
    CourseOutlineComponent,
)


class EducationPages:
    """教育领域页面模板"""

    @staticmethod
    def _create_course_outline_components() -> list:
        template = PageTemplate(name="course_outline", display_name="课程大纲", icon="book-open", category="education", description="课程整体结构规划")
        template.add_component(TextBlockComponent(id="title", content="课程大纲", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="规划课程模块、单元和学习目标。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(CourseOutlineComponent(
            id="course_modules",
            modules=[
                {"module_name": "模块一：基础概念", "units": [
                    {"title": "入门导论", "objective": "理解基本概念", "activities": "讲解+讨论", "duration": "2课时", "materials": ["教材第一章", "课件"]},
                ]},
                {"module_name": "模块二：核心知识", "units": [
                    {"title": "核心理论", "objective": "掌握核心理论", "activities": "案例分析", "duration": "4课时", "materials": ["教材第二章", "案例集"]},
                ]},
            ],
            order=3,
        ))
        template.add_component(TextBlockComponent(id="course_notes", content="教学备注：记录补充说明和教学建议。", sub_type="paragraph", placeholder="先修课程要求、考核方式、参考书目", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_lesson_plan_components() -> list:
        template = PageTemplate(name="lesson_plan", display_name="教案设计", icon="file-text", category="education", description="单节课详细教案")
        template.add_component(TextBlockComponent(id="title", content="教案设计", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="设计单节课的教学流程和活动安排。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(StepsComponent(
            id="lesson_steps",
            steps=[
                {"id": "warmup", "title": "课堂导入", "description": "复习旧知，引入新课", "status": "pending"},
                {"id": "present", "title": "知识讲授", "description": "核心内容讲解", "status": "pending"},
                {"id": "practice", "title": "课堂练习", "description": "学生自主练习", "status": "pending"},
                {"id": "summary", "title": "总结反馈", "description": "课堂小结与答疑", "status": "pending"},
            ],
            current=0,
            order=3,
        ))
        template.add_component(TableComponent(
            id="lesson_details",
            columns=[
                {"key": "phase", "title": "教学环节", "width": "15%"},
                {"key": "duration", "title": "时间", "width": "10%"},
                {"key": "activity", "title": "师生活动", "width": "40%"},
                {"key": "materials", "title": "教学资源", "width": "35%"},
            ],
            data=[
                {"phase": "导入", "duration": "5min", "activity": "提问回顾上节课内容", "materials": "PPT课件"},
                {"phase": "讲授", "duration": "20min", "activity": "讲解新知识点", "materials": "板书/多媒体"},
                {"phase": "练习", "duration": "15min", "activity": "分组讨论与练习", "materials": "练习册"},
            ],
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_student_progress_components() -> list:
        template = PageTemplate(name="student_progress", display_name="学生进度", icon="trending-up", category="education", description="学生学习进度跟踪")
        template.add_component(TextBlockComponent(id="title", content="学生进度", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="跟踪和评估学生的学习进度与完成情况。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(MetricCardComponent(
            id="overall_progress",
            value="75",
            label="整体完成率",
            suffix="%",
            trend="up",
            size="large",
            order=3,
        ))
        template.add_component(ProgressBarComponent(
            id="module_progress",
            percentage=60,
            style="bar",
            color="#1890FF",
            order=4,
        ))
        template.add_component(TableComponent(
            id="student_list",
            columns=[
                {"key": "name", "title": "学生姓名", "width": "20%"},
                {"key": "module", "title": "当前模块", "width": "20%"},
                {"key": "progress", "title": "进度", "width": "20%"},
                {"key": "score", "title": "平均成绩", "width": "15%"},
                {"key": "status", "title": "状态", "width": "25%"},
            ],
            data=[
                {"name": "学生A", "module": "模块二", "progress": "60%", "score": "85", "status": "正常"},
                {"name": "学生B", "module": "模块一", "progress": "40%", "score": "72", "status": "需关注"},
            ],
            order=5,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_assessment_score_components() -> list:
        template = PageTemplate(name="assessment_score", display_name="评估评分", icon="bar-chart", category="education", description="多维度评估评分表")
        template.add_component(TextBlockComponent(id="title", content="评估评分", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="多维度评估学生表现并进行评分。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(ScorecardComponent(
            id="assessment",
            dimensions=[
                {"name": "知识掌握", "weight": 0.3, "max_score": 100, "score": 85},
                {"name": "实践能力", "weight": 0.3, "max_score": 100, "score": 78},
                {"name": "课堂参与", "weight": 0.2, "max_score": 100, "score": 90},
                {"name": "团队合作", "weight": 0.2, "max_score": 100, "score": 82},
            ],
            score_type="numeric",
            order=3,
        ))
        template.add_component(TableComponent(
            id="grade_table",
            columns=[
                {"key": "student", "title": "学生", "width": "15%"},
                {"key": "knowledge", "title": "知识掌握", "width": "15%"},
                {"key": "practice", "title": "实践能力", "width": "15%"},
                {"key": "participation", "title": "课堂参与", "width": "15%"},
                {"key": "teamwork", "title": "团队合作", "width": "15%"},
                {"key": "total", "title": "总分", "width": "25%"},
            ],
            data=[
                {"student": "学生A", "knowledge": "85", "practice": "78", "participation": "90", "teamwork": "82", "total": "83.5"},
            ],
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_knowledge_graph_components() -> list:
        template = PageTemplate(name="knowledge_graph", display_name="知识图谱", icon="network", category="education", description="学科知识体系图谱")
        template.add_component(TextBlockComponent(id="title", content="知识图谱", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="构建学科知识点的层级结构和关联关系。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(MindmapComponent(
            id="knowledge_map",
            nodes=[
                {"id": "root", "label": "学科总纲", "parent_id": None, "color": "#1890FF"},
                {"id": "ch1", "label": "第一章基础", "parent_id": "root", "color": "#52C41A"},
                {"id": "ch2", "label": "第二章进阶", "parent_id": "root", "color": "#FAAD14"},
                {"id": "sec1", "label": "核心概念", "parent_id": "ch1", "color": "#13C2C2"},
                {"id": "sec2", "label": "基本定理", "parent_id": "ch1", "color": "#13C2C2"},
                {"id": "sec3", "label": "高级应用", "parent_id": "ch2", "color": "#EB2F96"},
            ],
            layout="tree",
            order=3,
        ))
        template.add_component(TextBlockComponent(id="graph_notes", content="图谱说明：标注重点难点和教学顺序。", sub_type="paragraph", placeholder="知识点之间的前置依赖关系、重点标记、建议学习顺序", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_classroom_activity_components() -> list:
        template = PageTemplate(name="classroom_activity", display_name="课堂活动", icon="users", category="education", description="课堂互动活动设计")
        template.add_component(TextBlockComponent(id="title", content="课堂活动", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="设计课堂互动活动和小组任务。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(ListComponent(
            id="activity_list",
            items=[
                {"label": "小组讨论", "value": "discussion", "description": "分组讨论核心问题并展示", "checked": False},
                {"label": "角色扮演", "value": "roleplay", "description": "模拟真实场景的应用实践", "checked": False},
                {"label": "快速问答", "value": "quiz", "description": "课堂即时测验检验理解", "checked": False},
                {"label": "案例分析", "value": "case", "description": "分析真实案例深化理解", "checked": False},
                {"label": "项目展示", "value": "presentation", "description": "小组项目成果展示与互评", "checked": False},
            ],
            show_checkbox=True,
            list_type="simple",
            order=3,
        ))
        template.add_component(TableComponent(
            id="activity_schedule",
            columns=[
                {"key": "time", "title": "时间", "width": "15%"},
                {"key": "activity", "title": "活动名称", "width": "25%"},
                {"key": "description", "title": "活动描述", "width": "35%"},
                {"key": "materials", "title": "所需材料", "width": "25%"},
            ],
            data=[
                {"time": "0-5min", "activity": "暖场活动", "description": "激发兴趣", "materials": "小道具"},
                {"time": "5-15min", "activity": "小组讨论", "description": "主题探讨", "materials": "讨论题卡"},
            ],
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    PAGE_TYPES = {
        "course_outline": {
            "name": "course_outline", "display_name": "课程大纲", "icon": "book-open",
            "category": "education", "description": "课程整体结构规划",
            "default_schema": {"modules": [], "components": _create_course_outline_components.__func__()}
        },
        "lesson_plan": {
            "name": "lesson_plan", "display_name": "教案设计", "icon": "file-text",
            "category": "education", "description": "单节课详细教案",
            "default_schema": {"plan": {}, "components": _create_lesson_plan_components.__func__()}
        },
        "student_progress": {
            "name": "student_progress", "display_name": "学生进度", "icon": "trending-up",
            "category": "education", "description": "学生学习进度跟踪",
            "default_schema": {"students": [], "components": _create_student_progress_components.__func__()}
        },
        "assessment_score": {
            "name": "assessment_score", "display_name": "评估评分", "icon": "bar-chart",
            "category": "education", "description": "多维度评估评分表",
            "default_schema": {"assessments": [], "components": _create_assessment_score_components.__func__()}
        },
        "knowledge_graph": {
            "name": "knowledge_graph", "display_name": "知识图谱", "icon": "network",
            "category": "education", "description": "学科知识体系图谱",
            "default_schema": {"nodes": [], "components": _create_knowledge_graph_components.__func__()}
        },
        "classroom_activity": {
            "name": "classroom_activity", "display_name": "课堂活动", "icon": "users",
            "category": "education", "description": "课堂互动活动设计",
            "default_schema": {"activities": [], "components": _create_classroom_activity_components.__func__()}
        },
    }
