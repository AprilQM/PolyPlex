"""
通用页面模板 - 使用新组件系统构建
包含6种通用页面类型：会议纪要、项目复盘、周报、知识库、自由笔记、团队通讯录
"""

from app.page_components import (
    PageTemplate,
    TextBlockComponent,
    DividerComponent,
    SpacerComponent,
    TableComponent,
    ListComponent,
    TimelineComponent,
    ProgressBarComponent,
    ScorecardComponent,
    TagSetComponent,
    CommentAnchorComponent,
)


class GeneralPages:
    """通用页面模板 - 6种页面类型"""

    @staticmethod
    def _create_meeting_minutes_components() -> list:
        """创建会议纪要页面的组件列表"""
        template = PageTemplate(
            name="meeting_minutes",
            display_name="会议纪要",
            icon="calendar",
            category="general",
            description="记录会议议程、讨论内容和行动项",
        )

        template.add_component(TextBlockComponent(
            id="meeting_minutes_title",
            content="会议纪要",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="meeting_minutes_desc",
            content="记录会议的基本信息、议程、讨论要点和待办事项。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="meeting_info",
            title="会议基本信息",
            columns=[
                {"key": "field", "title": "字段", "width": "20%"},
                {"key": "value", "title": "内容", "width": "80%"},
            ],
            data=[
                {"field": "会议主题", "value": "请输入会议主题"},
                {"field": "日期时间", "value": "请输入会议时间"},
                {"field": "地点", "value": "请输入会议地点"},
                {"field": "主持人", "value": "请输入主持人"},
                {"field": "参会人员", "value": "请输入参会人员"},
                {"field": "记录人", "value": "请输入记录人"},
            ],
            order=3,
        ))

        template.add_component(DividerComponent(order=4))

        template.add_component(TextBlockComponent(
            id="agenda_section",
            content="会议议程",
            sub_type="heading",
            level=2,
            order=5,
        ))

        template.add_component(ListComponent(
            id="agenda_items",
            title="议程列表",
            items=[
                {"label": "议程一", "value": "item_1", "description": "请填写议程内容"},
                {"label": "议程二", "value": "item_2", "description": "请填写议程内容"},
                {"label": "议程三", "value": "item_3", "description": "请填写议程内容"},
            ],
            list_type="sorted",
            order=6,
        ))

        template.add_component(TextBlockComponent(
            id="action_items_section",
            content="行动项",
            sub_type="heading",
            level=2,
            order=7,
        ))

        template.add_component(TableComponent(
            id="action_items",
            title="待办事项",
            columns=[
                {"key": "task", "title": "任务", "width": "30%"},
                {"key": "assignee", "title": "负责人", "width": "20%"},
                {"key": "deadline", "title": "截止日期", "width": "20%"},
                {"key": "status", "title": "状态", "width": "15%"},
                {"key": "notes", "title": "备注", "width": "15%"},
            ],
            data=[
                {"task": "请填写任务描述", "assignee": "请填写负责人", "deadline": "请填写截止日期", "status": "待处理", "notes": ""},
            ],
            order=8,
        ))

        template.add_component(CommentAnchorComponent(
            id="meeting_comments",
            comments=[],
            allow_comment=True,
            placeholder="添加评论...",
            order=9,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_project_review_components() -> list:
        """创建项目复盘页面的组件列表"""
        template = PageTemplate(
            name="project_review",
            display_name="项目复盘",
            icon="refresh",
            category="general",
            description="项目回顾与经验总结文档",
        )

        template.add_component(TextBlockComponent(
            id="project_review_title",
            content="项目复盘",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="project_review_desc",
            content="对已完成项目进行回顾总结，分析做得好的方面和改进空间，提炼经验教训。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="review_basic_info",
            title="项目基本信息",
            columns=[
                {"key": "field", "title": "字段", "width": "20%"},
                {"key": "value", "title": "内容", "width": "80%"},
            ],
            data=[
                {"field": "项目名称", "value": "请输入项目名称"},
                {"field": "项目周期", "value": "请输入项目周期"},
                {"field": "项目目标", "value": "请填写项目目标"},
                {"field": "实际成果", "value": "请填写实际成果"},
            ],
            order=3,
        ))

        template.add_component(DividerComponent(order=4))

        template.add_component(ScorecardComponent(
            id="review_scorecard",
            title="项目评分",
            dimensions=[
                {"name": "目标达成", "weight": 1.0, "max_score": 5, "score": 0},
                {"name": "进度管理", "weight": 1.0, "max_score": 5, "score": 0},
                {"name": "质量把控", "weight": 1.0, "max_score": 5, "score": 0},
                {"name": "团队协作", "weight": 1.0, "max_score": 5, "score": 0},
                {"name": "成本控制", "weight": 1.0, "max_score": 5, "score": 0},
            ],
            score_type="star",
            order=5,
        ))

        template.add_component(DividerComponent(order=6))

        template.add_component(TextBlockComponent(
            id="good_points_section",
            content="做得好的方面",
            sub_type="heading",
            level=2,
            order=7,
        ))

        template.add_component(ListComponent(
            id="good_points",
            items=[
                {"label": "", "value": "point_1", "description": "请描述做得好的地方"},
                {"label": "", "value": "point_2", "description": "请描述做得好的地方"},
            ],
            list_type="simple",
            show_checkbox=False,
            order=8,
        ))

        template.add_component(TextBlockComponent(
            id="improve_section",
            content="改进空间",
            sub_type="heading",
            level=2,
            order=9,
        ))

        template.add_component(ListComponent(
            id="improve_points",
            items=[
                {"label": "", "value": "improve_1", "description": "请描述需要改进的地方"},
                {"label": "", "value": "improve_2", "description": "请描述需要改进的地方"},
            ],
            list_type="simple",
            show_checkbox=False,
            order=10,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_weekly_report_components() -> list:
        """创建周报页面的组件列表"""
        template = PageTemplate(
            name="weekly_report",
            display_name="周报",
            icon="clock",
            category="general",
            description="每周工作进展汇报",
        )

        template.add_component(TextBlockComponent(
            id="weekly_report_title",
            content="周报",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="weekly_report_desc",
            content="汇报本周工作进展、下周计划和遇到的问题。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="weekly_info",
            title="周报基本信息",
            columns=[
                {"key": "field", "title": "字段", "width": "15%"},
                {"key": "value", "title": "内容", "width": "85%"},
            ],
            data=[
                {"field": "汇报人", "value": "请输入姓名"},
                {"field": "汇报周期", "value": "请选择日期范围"},
                {"field": "部门/项目", "value": "请输入部门或项目名称"},
            ],
            order=3,
        ))

        template.add_component(DividerComponent(order=4))

        template.add_component(TextBlockComponent(
            id="this_week_section",
            content="本周工作",
            sub_type="heading",
            level=2,
            order=5,
        ))

        template.add_component(ListComponent(
            id="this_week_tasks",
            title="本周完成事项",
            items=[
                {"label": "", "value": "task_1", "description": "请填写本周完成的工作"},
                {"label": "", "value": "task_2", "description": "请填写本周完成的工作"},
                {"label": "", "value": "task_3", "description": "请填写本周完成的工作"},
            ],
            list_type="simple",
            show_checkbox=True,
            order=6,
        ))

        template.add_component(ProgressBarComponent(
            id="weekly_progress",
            percentage=50,
            style="bar",
            color="#1890FF",
            show_label=True,
            order=7,
        ))

        template.add_component(TextBlockComponent(
            id="next_week_section",
            content="下周计划",
            sub_type="heading",
            level=2,
            order=8,
        ))

        template.add_component(ListComponent(
            id="next_week_tasks",
            title="下周计划事项",
            items=[
                {"label": "", "value": "plan_1", "description": "请填写下周计划"},
                {"label": "", "value": "plan_2", "description": "请填写下周计划"},
            ],
            list_type="sorted",
            order=9,
        ))

        template.add_component(TextBlockComponent(
            id="issues_section",
            content="问题与风险",
            sub_type="heading",
            level=2,
            order=10,
        ))

        template.add_component(ListComponent(
            id="issues_list",
            items=[
                {"label": "", "value": "issue_1", "description": "请描述遇到的问题或风险"},
            ],
            list_type="simple",
            order=11,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_knowledge_base_components() -> list:
        """创建知识库页面的组件列表"""
        template = PageTemplate(
            name="knowledge_base",
            display_name="知识库",
            icon="book",
            category="general",
            description="团队知识沉淀与文档管理",
        )

        template.add_component(TextBlockComponent(
            id="knowledge_base_title",
            content="知识库",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="knowledge_base_desc",
            content="团队知识沉淀、技术文档、最佳实践和学习资料的集中管理空间。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TagSetComponent(
            id="kb_tags",
            title="知识分类",
            tags=[
                {"name": "技术文档", "color": "#1890FF"},
                {"name": "产品设计", "color": "#52C41A"},
                {"name": "项目管理", "color": "#FAAD14"},
                {"name": "运营策略", "color": "#FF4D4F"},
                {"name": "行业研究", "color": "#722ED1"},
            ],
            allow_create=True,
            order=3,
        ))

        template.add_component(DividerComponent(order=4))

        template.add_component(TableComponent(
            id="kb_articles",
            title="知识文档列表",
            columns=[
                {"key": "title", "title": "文档标题", "width": "30%"},
                {"key": "category", "title": "分类", "width": "15%"},
                {"key": "author", "title": "作者", "width": "15%"},
                {"key": "updated", "title": "更新时间", "width": "15%"},
                {"key": "status", "title": "状态", "width": "10%"},
                {"key": "actions", "title": "操作", "width": "15%"},
            ],
            data=[
                {"title": "请添加知识文档", "category": "请选择分类", "author": "请填写作者", "updated": "请填写日期", "status": "草稿", "actions": "查看"},
            ],
            order=5,
        ))

        template.add_component(CommentAnchorComponent(
            id="kb_comments",
            comments=[],
            allow_comment=True,
            placeholder="对知识库内容发表评论...",
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_free_note_components() -> list:
        """创建自由笔记页面的组件列表"""
        template = PageTemplate(
            name="free_note",
            display_name="自由笔记",
            icon="edit",
            category="general",
            description="自由记录想法、灵感和笔记",
        )

        template.add_component(TextBlockComponent(
            id="free_note_title",
            content="自由笔记",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="free_note_content",
            content="",
            sub_type="paragraph",
            placeholder="在这里自由记录你的想法、灵感或笔记...",
            order=1,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_team_directory_components() -> list:
        """创建团队通讯录页面的组件列表"""
        template = PageTemplate(
            name="team_directory",
            display_name="团队通讯录",
            icon="users",
            category="general",
            description="团队成员联系方式与信息一览",
        )

        template.add_component(TextBlockComponent(
            id="team_directory_title",
            content="团队通讯录",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="team_directory_desc",
            content="团队成员信息、角色分工和联系方式汇总。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="team_members",
            title="团队成员列表",
            columns=[
                {"key": "name", "title": "姓名", "width": "12%"},
                {"key": "role", "title": "角色", "width": "15%"},
                {"key": "department", "title": "部门", "width": "15%"},
                {"key": "email", "title": "邮箱", "width": "20%"},
                {"key": "phone", "title": "电话", "width": "18%"},
                {"key": "skills", "title": "技能标签", "width": "20%"},
            ],
            data=[
                {"name": "请填写姓名", "role": "请填写角色", "department": "请填写部门", "email": "请填写邮箱", "phone": "请填写电话", "skills": "请填写技能标签"},
            ],
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # PAGE_TYPES 字典
    PAGE_TYPES = {
        "meeting_minutes": {
            "name": "meeting_minutes",
            "display_name": "会议纪要",
            "icon": "calendar",
            "category": "general",
            "description": "记录会议议程、讨论内容和行动项",
            "default_schema": {
                "meeting_info": {},
                "agenda": [],
                "action_items": [],
                "components": _create_meeting_minutes_components.__func__(),
            }
        },
        "project_review": {
            "name": "project_review",
            "display_name": "项目复盘",
            "icon": "refresh",
            "category": "general",
            "description": "项目回顾与经验总结文档",
            "default_schema": {
                "basic_info": {},
                "good_points": [],
                "improve_points": [],
                "components": _create_project_review_components.__func__(),
            }
        },
        "weekly_report": {
            "name": "weekly_report",
            "display_name": "周报",
            "icon": "clock",
            "category": "general",
            "description": "每周工作进展汇报",
            "default_schema": {
                "this_week": [],
                "next_week": [],
                "issues": [],
                "progress": 0,
                "components": _create_weekly_report_components.__func__(),
            }
        },
        "knowledge_base": {
            "name": "knowledge_base",
            "display_name": "知识库",
            "icon": "book",
            "category": "general",
            "description": "团队知识沉淀与文档管理",
            "default_schema": {
                "articles": [],
                "tags": [],
                "components": _create_knowledge_base_components.__func__(),
            }
        },
        "free_note": {
            "name": "free_note",
            "display_name": "自由笔记",
            "icon": "edit",
            "category": "general",
            "description": "自由记录想法、灵感和笔记",
            "default_schema": {
                "content": "",
                "format": "plain",
                "components": _create_free_note_components.__func__(),
            }
        },
        "team_directory": {
            "name": "team_directory",
            "display_name": "团队通讯录",
            "icon": "users",
            "category": "general",
            "description": "团队成员联系方式与信息一览",
            "default_schema": {
                "members": [],
                "components": _create_team_directory_components.__func__(),
            }
        },
    }
