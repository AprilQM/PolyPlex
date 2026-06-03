"""
其他领域页面模板 - 使用组件构建
"""
from app.page_components import (
    PageTemplate,
    TextBlockComponent, ImageGalleryComponent,
    TableComponent, KanbanComponent, TimelineComponent, StepsComponent, ListComponent,
    MindmapComponent, FlowchartComponent, RelationGraphComponent, DataChartComponent, MoodboardComponent, WhiteboardComponent,
    MetricCardComponent, ProgressBarComponent, CounterComponent, ScorecardComponent, FormulaComponent,
    CommentAnchorComponent, VoteModuleComponent, TaskAssignComponent,
    PageRefComponent, EmbedViewComponent, TagSetComponent,
    DividerComponent, SpacerComponent, MultiColumnComponent, TabsComponent,
)


class OtherPages:
    """其他领域页面模板"""

    @staticmethod
    def _create_event_plan_components() -> list:
        """创建活动方案页面的组件列表"""
        template = PageTemplate(
            name="event_plan",
            display_name="活动方案",
            icon="calendar",
            category="other",
            description="活动策划和执行方案",
        )

        template.add_component(TextBlockComponent(
            id="event_plan_title",
            content="活动方案",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="event_plan_desc",
            content="详细的活动策划方案，包含流程、预算和人员分工。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TimelineComponent(
            id="event_timeline",
            events=[
                {"id": "phase_1", "title": "筹备期", "description": "确定方案、预订场地", "date": "活动前 30 天", "icon": "clock"},
                {"id": "phase_2", "title": "准备期", "description": "物资采购、人员分工", "date": "活动前 14 天", "icon": "tool"},
                {"id": "phase_3", "title": "冲刺期", "description": "场地布置、彩排", "date": "活动前 3 天", "icon": "rocket"},
                {"id": "phase_4", "title": "执行期", "description": "活动当天执行", "date": "活动日", "icon": "play"},
                {"id": "phase_5", "title": "收尾期", "description": "总结复盘、结算", "date": "活动后 7 天", "icon": "check"},
            ],
            layout="vertical",
            order=3,
        ))

        template.add_component(ListComponent(
            id="event_overview",
            items=[
                {"label": "活动主题", "value": "theme", "description": "年度总结大会", "icon": "star"},
                {"label": "活动日期", "value": "date", "description": "2024-06-15", "icon": "calendar"},
                {"label": "活动地点", "value": "location", "description": "XX 会议中心 3 楼", "icon": "map"},
                {"label": "预计参与人数", "value": "attendees", "description": "200 人", "icon": "users"},
                {"label": "预算总额", "value": "budget", "description": "50,000 元", "icon": "dollar"},
            ],
            list_type="property",
            order=4,
        ))

        template.add_component(TableComponent(
            id="event_budget",
            columns=[
                {"key": "item", "title": "项目", "width": "30%"},
                {"key": "estimated", "title": "预算金额", "width": "20%"},
                {"key": "actual", "title": "实际支出", "width": "20%"},
                {"key": "difference", "title": "差额", "width": "15%"},
                {"key": "notes", "title": "备注", "width": "15%"},
            ],
            data=[
                {"item": "场地租赁", "estimated": "15000", "actual": "15000", "difference": "0", "notes": ""},
                {"item": "餐饮茶歇", "estimated": "10000", "actual": "8500", "difference": "-1500", "notes": "优惠"},
                {"item": "物料制作", "estimated": "8000", "actual": "8000", "difference": "0", "notes": ""},
                {"item": "人员劳务", "estimated": "12000", "actual": "12500", "difference": "+500", "notes": "加班费"},
                {"item": "其他", "estimated": "5000", "actual": "3200", "difference": "-1800", "notes": "节约"},
            ],
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_material_list_components() -> list:
        """创建物资清单页面的组件列表"""
        template = PageTemplate(
            name="material_list",
            display_name="物资清单",
            icon="box",
            category="other",
            description="活动物资准备和管理",
        )

        template.add_component(TextBlockComponent(
            id="material_list_title",
            content="物资清单",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="material_list_desc",
            content="管理活动所需的物资，包括采购、入库和领用。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MetricCardComponent(
            id="material_metrics",
            value="32",
            label="物资总数",
            prefix="",
            suffix="件",
            trend="+8",
            size="medium",
            order=3,
        ))

        template.add_component(TableComponent(
            id="material_table",
            columns=[
                {"key": "name", "title": "物品名称", "width": "20%"},
                {"key": "category", "title": "类别", "width": "15%"},
                {"key": "quantity", "title": "数量", "width": "15%"},
                {"key": "status", "title": "状态", "width": "15%"},
                {"key": "responsible", "title": "负责人", "width": "20%"},
                {"key": "notes", "title": "备注", "width": "15%"},
            ],
            data=[
                {"name": "横幅", "category": "宣传", "quantity": "2 条", "status": "已准备", "responsible": "张三", "notes": ""},
                {"name": "签到表", "category": "文档", "quantity": "3 份", "status": "已准备", "responsible": "李四", "notes": "打印 50 份"},
                {"name": "胸牌", "category": "物料", "quantity": "50 个", "status": "采购中", "responsible": "张三", "notes": "定制"},
                {"name": "礼品袋", "category": "物料", "quantity": "50 个", "status": "待采购", "responsible": "王五", "notes": "预算内"},
                {"name": "投影仪", "category": "设备", "quantity": "1 台", "status": "已借用", "responsible": "李四", "notes": "确认可用"},
            ],
            order=4,
        ))

        template.add_component(ListComponent(
            id="material_categories",
            items=[
                {"label": "宣传物料", "value": "promotion", "description": "2 件", "icon": "flag", "checked": True},
                {"label": "文档资料", "value": "docs", "description": "3 件", "icon": "file", "checked": True},
                {"label": "活动物料", "value": "supplies", "description": "6 件", "icon": "box", "checked": False},
                {"label": "电子设备", "value": "devices", "description": "5 件", "icon": "monitor", "checked": True},
                {"label": "食品饮料", "value": "food", "description": "8 件", "icon": "coffee", "checked": False},
            ],
            list_type="simple",
            show_checkbox=True,
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_staff_division_components() -> list:
        """创建人员分工页面的组件列表"""
        template = PageTemplate(
            name="staff_division",
            display_name="人员分工",
            icon="users",
            category="other",
            description="人员任务分配和管理",
        )

        template.add_component(TextBlockComponent(
            id="staff_division_title",
            content="人员分工",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="staff_division_desc",
            content="明确团队成员的分工和职责，追踪任务进度。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="staff_table",
            columns=[
                {"key": "name", "title": "姓名", "width": "15%"},
                {"key": "role", "title": "角色", "width": "15%"},
                {"key": "tasks", "title": "负责任务", "width": "35%"},
                {"key": "deadline", "title": "截止日期", "width": "15%"},
                {"key": "status", "title": "状态", "width": "20%"},
            ],
            data=[
                {"name": "张三", "role": "总负责人", "tasks": "整体协调、预算管理", "deadline": "活动当天", "status": "进行中"},
                {"name": "李四", "role": "后勤组长", "tasks": "物资采购、场地布置", "deadline": "活动前 3 天", "status": "进行中"},
                {"name": "王五", "role": "宣传组长", "tasks": "海报设计、宣传推广", "deadline": "活动前 7 天", "status": "已完成"},
                {"name": "赵六", "role": "现场执行", "tasks": "签到接待、流程引导", "deadline": "活动当天", "status": "待开始"},
            ],
            order=3,
        ))

        template.add_component(KanbanComponent(
            id="staff_kanban",
            columns=[
                {"id": "todo", "title": "待办", "color": "gray"},
                {"id": "in_progress", "title": "进行中", "color": "blue"},
                {"id": "done", "title": "已完成", "color": "green"},
            ],
            cards=[
                {"id": "card_1", "title": "场地布置方案", "description": "负责人：李四", "column_id": "in_progress"},
                {"id": "card_2", "title": "海报设计", "description": "负责人：王五", "column_id": "done"},
                {"id": "card_3", "title": "签到流程确认", "description": "负责人：赵六", "column_id": "todo"},
                {"id": "card_4", "title": "预算审批", "description": "负责人：张三", "column_id": "in_progress"},
            ],
            order=4,
        ))

        template.add_component(TaskAssignComponent(
            id="staff_task",
            assignee="张三",
            status="in_progress",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_custom_components() -> list:
        """创建自定义页面模板的组件列表"""
        template = PageTemplate(
            name="custom",
            display_name="自定义",
            icon="edit",
            category="other",
            description="自由定义的空白页面",
        )

        template.add_component(TextBlockComponent(
            id="custom_title",
            content="自定义页面",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="custom_desc",
            content="自由定义页面内容，按需添加各种组件。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TextBlockComponent(
            id="custom_content",
            content="",
            sub_type="paragraph",
            placeholder="在此自由编写内容...",
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    # PAGE_TYPES 字典
    PAGE_TYPES = {
        "event_plan": {
            "name": "event_plan",
            "display_name": "活动方案",
            "icon": "calendar",
            "category": "other",
            "description": "活动策划和执行方案",
            "default_schema": {
                "components": _create_event_plan_components.__func__(),
            }
        },
        "material_list": {
            "name": "material_list",
            "display_name": "物资清单",
            "icon": "box",
            "category": "other",
            "description": "活动物资准备和管理",
            "default_schema": {
                "components": _create_material_list_components.__func__(),
            }
        },
        "staff_division": {
            "name": "staff_division",
            "display_name": "人员分工",
            "icon": "users",
            "category": "other",
            "description": "人员任务分配和管理",
            "default_schema": {
                "components": _create_staff_division_components.__func__(),
            }
        },
        "custom": {
            "name": "custom",
            "display_name": "自定义",
            "icon": "edit",
            "category": "other",
            "description": "自由定义的空白页面",
            "default_schema": {
                "components": _create_custom_components.__func__(),
            }
        },
    }
