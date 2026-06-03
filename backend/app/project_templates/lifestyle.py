"""
生活/个人领域页面模板 - 使用组件构建
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


class LifestylePages:
    """生活/个人领域页面模板"""

    @staticmethod
    def _create_travel_board_components() -> list:
        """创建旅行灵感板页面的组件列表"""
        template = PageTemplate(
            name="travel_board",
            display_name="旅行灵感板",
            icon="compass",
            category="lifestyle",
            description="旅行目的地灵感和规划",
        )

        template.add_component(TextBlockComponent(
            id="travel_board_title",
            content="旅行灵感板",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="travel_board_desc",
            content="收集旅行目的地灵感，规划行程和预算。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MoodboardComponent(
            id="travel_moodboard",
            items=[
                {"id": "item_1", "type": "image", "content": "目的地风景", "position": {"x": 0, "y": 0}},
                {"id": "item_2", "type": "text", "content": "旅行灵感与想法", "position": {"x": 300, "y": 0}},
                {"id": "item_3", "type": "image", "content": "参考行程", "position": {"x": 0, "y": 200}},
            ],
            order=3,
        ))

        template.add_component(ImageGalleryComponent(
            id="travel_images",
            images=[
                {"url": "", "caption": "目的地风景 1", "alt": "destination_1"},
                {"url": "", "caption": "目的地风景 2", "alt": "destination_2"},
                {"url": "", "caption": "目的地美食", "alt": "local_food"},
            ],
            layout="grid",
            columns=3,
            order=4,
        ))

        template.add_component(ListComponent(
            id="travel_checklist",
            items=[
                {"label": "办理签证", "value": "visa", "description": "提前 1 个月申请", "icon": "file", "checked": False},
                {"label": "预订机票", "value": "flight", "description": "比价平台筛选", "icon": "plane", "checked": False},
                {"label": "预订住宿", "value": "hotel", "description": "市中心民宿", "icon": "home", "checked": True},
                {"label": "购买保险", "value": "insurance", "description": "旅行意外险", "icon": "shield", "checked": False},
            ],
            list_type="simple",
            show_checkbox=True,
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_recipe_dev_components() -> list:
        """创建食谱开发页面的组件列表"""
        template = PageTemplate(
            name="recipe_dev",
            display_name="食谱开发",
            icon="food",
            category="lifestyle",
            description="菜谱研发和配方管理",
        )

        template.add_component(TextBlockComponent(
            id="recipe_dev_title",
            content="食谱开发",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="recipe_dev_desc",
            content="记录和开发新的食谱，管理配方、步骤和试吃反馈。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="recipe_ingredients",
            columns=[
                {"key": "name", "title": "食材", "width": "30%"},
                {"key": "quantity", "title": "用量", "width": "20%"},
                {"key": "prep", "title": "预处理", "width": "30%"},
                {"key": "notes", "title": "备注", "width": "20%"},
            ],
            data=[
                {"name": "面粉", "quantity": "200g", "prep": "过筛", "notes": "高筋面粉"},
                {"name": "鸡蛋", "quantity": "3 个", "prep": "室温回温", "notes": ""},
                {"name": "黄油", "quantity": "50g", "prep": "软化", "notes": "无盐黄油"},
                {"name": "糖", "quantity": "80g", "prep": "", "notes": "细砂糖"},
            ],
            order=3,
        ))

        template.add_component(StepsComponent(
            id="recipe_steps",
            steps=[
                {"id": "step_1", "title": "准备材料", "description": "将所有食材按用量准备好", "status": "completed"},
                {"id": "step_2", "title": "混合干料", "description": "将面粉、糖等干性材料混合均匀", "status": "completed"},
                {"id": "step_3", "title": "加入湿料", "description": "将鸡蛋、黄油等湿性材料加入搅拌", "status": "in_progress"},
                {"id": "step_4", "title": "烘烤", "description": "180 度预热，烘烤 25 分钟", "status": "pending"},
                {"id": "step_5", "title": "装饰摆盘", "description": "冷却后装饰", "status": "pending"},
            ],
            current=2,
            order=4,
        ))

        template.add_component(ImageGalleryComponent(
            id="recipe_images",
            images=[
                {"url": "", "caption": "成品参考图", "alt": "final_dish"},
                {"url": "", "caption": "制作过程", "alt": "cooking_process"},
            ],
            layout="grid",
            columns=2,
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_renovation_inspire_components() -> list:
        """创建装修灵感板页面的组件列表"""
        template = PageTemplate(
            name="renovation_inspire",
            display_name="装修灵感板",
            icon="home",
            category="lifestyle",
            description="家居装修灵感和规划",
        )

        template.add_component(TextBlockComponent(
            id="renovation_inspire_title",
            content="装修灵感板",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="renovation_inspire_desc",
            content="收集装修风格灵感，规划空间布局和材料清单。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MoodboardComponent(
            id="renovation_moodboard",
            items=[
                {"id": "item_1", "type": "image", "content": "客厅风格参考", "position": {"x": 0, "y": 0}},
                {"id": "item_2", "type": "color", "content": "#F5F5DC", "position": {"x": 250, "y": 0}},
                {"id": "item_3", "type": "color", "content": "#8B7355", "position": {"x": 250, "y": 100}},
                {"id": "item_4", "type": "text", "content": "北欧简约风格", "position": {"x": 0, "y": 200}},
                {"id": "item_5", "type": "image", "content": "厨房设计方案", "position": {"x": 300, "y": 200}},
            ],
            order=3,
        ))

        template.add_component(ImageGalleryComponent(
            id="renovation_images",
            images=[
                {"url": "", "caption": "客厅设计参考", "alt": "living_room"},
                {"url": "", "caption": "卧室设计参考", "alt": "bedroom"},
                {"url": "", "caption": "厨房设计参考", "alt": "kitchen"},
                {"url": "", "caption": "卫生间设计参考", "alt": "bathroom"},
            ],
            layout="grid",
            columns=4,
            order=4,
        ))

        template.add_component(ListComponent(
            id="renovation_tasks",
            items=[
                {"label": "水电改造", "value": "electrical", "description": "布线规划、水管铺设", "icon": "tool", "checked": False},
                {"label": "墙面处理", "value": "wall", "description": "铲墙、刷漆、贴壁纸", "icon": "tool", "checked": False},
                {"label": "地面铺设", "value": "floor", "description": "地板/瓷砖铺设", "icon": "tool", "checked": False},
                {"label": "家具选购", "value": "furniture", "description": "沙发、床、柜子", "icon": "tool", "checked": False},
                {"label": "软装搭配", "value": "decor", "description": "窗帘、灯具、装饰", "icon": "tool", "checked": False},
            ],
            list_type="simple",
            show_checkbox=True,
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_fitness_plan_components() -> list:
        """创建健身计划页面的组件列表"""
        template = PageTemplate(
            name="fitness_plan",
            display_name="健身计划",
            icon="activity",
            category="lifestyle",
            description="训练计划和健身追踪",
        )

        template.add_component(TextBlockComponent(
            id="fitness_plan_title",
            content="健身计划",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="fitness_plan_desc",
            content="制定训练计划，追踪健身进度和身体变化。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="workout_schedule",
            columns=[
                {"key": "day", "title": "日期", "width": "15%"},
                {"key": "focus", "title": "训练部位", "width": "20%"},
                {"key": "exercises", "title": "训练内容", "width": "35%"},
                {"key": "duration", "title": "时长", "width": "15%"},
                {"key": "status", "title": "状态", "width": "15%"},
            ],
            data=[
                {"day": "周一", "focus": "胸部", "exercises": "卧推、飞鸟、俯卧撑", "duration": "60min", "status": "已完成"},
                {"day": "周二", "focus": "背部", "exercises": "引体向上、划船、硬拉", "duration": "60min", "status": "已完成"},
                {"day": "周三", "focus": "休息", "exercises": "有氧运动", "duration": "30min", "status": "待完成"},
                {"day": "周四", "focus": "肩部", "exercises": "推举、侧平举、前平举", "duration": "50min", "status": "待完成"},
                {"day": "周五", "focus": "腿部", "exercises": "深蹲、腿举、弓步", "duration": "60min", "status": "待完成"},
            ],
            order=3,
        ))

        template.add_component(MetricCardComponent(
            id="fitness_metrics",
            value="75",
            label="本周训练完成率",
            prefix="",
            suffix="%",
            trend="+5%",
            size="medium",
            order=4,
        ))

        template.add_component(ProgressBarComponent(
            id="fitness_progress",
            percentage=60.0,
            style="bar",
            color="green",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_yearly_goals_components() -> list:
        """创建年度目标页面的组件列表"""
        template = PageTemplate(
            name="yearly_goals",
            display_name="年度目标",
            icon="target",
            category="lifestyle",
            description="年度目标和里程碑追踪",
        )

        template.add_component(TextBlockComponent(
            id="yearly_goals_title",
            content="年度目标",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="yearly_goals_desc",
            content="设定年度目标，分解为季度里程碑，追踪完成进度。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(StepsComponent(
            id="yearly_milestones",
            steps=[
                {"id": "q1", "title": "第一季度", "description": "基础建设", "status": "completed"},
                {"id": "q2", "title": "第二季度", "description": "稳步推进", "status": "in_progress"},
                {"id": "q3", "title": "第三季度", "description": "加速冲刺", "status": "pending"},
                {"id": "q4", "title": "第四季度", "description": "收官总结", "status": "pending"},
            ],
            current=1,
            order=3,
        ))

        template.add_component(ListComponent(
            id="goal_list",
            items=[
                {"label": "职业发展", "value": "career", "description": "完成专业认证考试，进度 40%", "icon": "briefcase", "checked": False},
                {"label": "健康健身", "value": "health", "description": "减重 5kg 并保持规律运动，进度 60%", "icon": "heart", "checked": False},
                {"label": "学习成长", "value": "learning", "description": "阅读 24 本书，进度 25%", "icon": "book", "checked": False},
                {"label": "财务管理", "value": "finance", "description": "储蓄达到目标额，进度 35%", "icon": "dollar", "checked": False},
                {"label": "旅行计划", "value": "travel", "description": "完成 2 次旅行，进度 50%", "icon": "globe", "checked": False},
            ],
            list_type="definition",
            order=4,
        ))

        template.add_component(ProgressBarComponent(
            id="overall_progress",
            percentage=42.0,
            style="dashboard",
            color="blue",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_learning_roadmap_components() -> list:
        """创建学习路线图页面的组件列表"""
        template = PageTemplate(
            name="learning_roadmap",
            display_name="学习路线图",
            icon="book",
            category="lifestyle",
            description="学习规划和技能路线图",
        )

        template.add_component(TextBlockComponent(
            id="learning_roadmap_title",
            content="学习路线图",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="learning_roadmap_desc",
            content="规划学习路径，追踪技能掌握进度。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TimelineComponent(
            id="learning_timeline",
            events=[
                {"id": "month_1", "title": "第 1-2 月：基础入门", "description": "掌握核心概念和基础知识", "date": "Q1", "icon": "book"},
                {"id": "month_3", "title": "第 3-4 月：实践进阶", "description": "完成小型实战项目", "date": "Q1", "icon": "code"},
                {"id": "month_5", "title": "第 5-6 月：深入专题", "description": "专攻高级知识点", "date": "Q2", "icon": "star"},
                {"id": "month_7", "title": "第 7-8 月：项目实战", "description": "参与真实项目开发", "date": "Q2", "icon": "rocket"},
                {"id": "month_9", "title": "第 9-10 月：总结输出", "description": "整理知识体系，输出博客", "date": "Q3", "icon": "write"},
                {"id": "month_11", "title": "第 11-12 月：持续进阶", "description": "探索前沿技术方向", "date": "Q3", "icon": "compass"},
            ],
            layout="vertical",
            order=3,
        ))

        template.add_component(StepsComponent(
            id="learning_steps",
            steps=[
                {"id": "beginner", "title": "初学者", "description": "基础知识掌握", "status": "completed"},
                {"id": "intermediate", "title": "进阶者", "description": "独立完成项目", "status": "in_progress"},
                {"id": "advanced", "title": "熟练者", "description": "解决复杂问题", "status": "pending"},
                {"id": "expert", "title": "专家", "description": "输出知识体系", "status": "pending"},
            ],
            current=1,
            order=4,
        ))

        template.add_component(ProgressBarComponent(
            id="learning_progress",
            percentage=35.0,
            style="bar",
            color="purple",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_budget_plan_components() -> list:
        """创建预算计划页面的组件列表"""
        template = PageTemplate(
            name="budget_plan",
            display_name="预算计划",
            icon="wallet",
            category="lifestyle",
            description="个人收支预算管理",
        )

        template.add_component(TextBlockComponent(
            id="budget_plan_title",
            content="预算计划",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="budget_plan_desc",
            content="管理个人收支预算，追踪消费和储蓄目标。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MetricCardComponent(
            id="budget_metrics",
            value="35000",
            label="本月预算总额",
            prefix="¥",
            suffix="",
            trend="-5%",
            size="large",
            order=3,
        ))

        template.add_component(TableComponent(
            id="budget_table",
            columns=[
                {"key": "category", "title": "类别", "width": "20%"},
                {"key": "budgeted", "title": "预算金额", "width": "20%"},
                {"key": "spent", "title": "已支出", "width": "20%"},
                {"key": "remaining", "title": "剩余", "width": "20%"},
                {"key": "progress", "title": "进度", "width": "20%"},
            ],
            data=[
                {"category": "住房", "budgeted": "8000", "spent": "8000", "remaining": "0", "progress": "100%"},
                {"category": "餐饮", "budgeted": "6000", "spent": "3200", "remaining": "2800", "progress": "53%"},
                {"category": "交通", "budgeted": "2000", "spent": "800", "remaining": "1200", "progress": "40%"},
                {"category": "娱乐", "budgeted": "3000", "spent": "1500", "remaining": "1500", "progress": "50%"},
                {"category": "储蓄", "budgeted": "10000", "spent": "5000", "remaining": "5000", "progress": "50%"},
                {"category": "其他", "budgeted": "6000", "spent": "1200", "remaining": "4800", "progress": "20%"},
            ],
            order=4,
        ))

        template.add_component(DataChartComponent(
            id="budget_chart",
            chart_type="pie",
            labels=["住房", "餐饮", "交通", "娱乐", "储蓄", "其他"],
            datasets=[{"label": "月度支出", "data": [8000, 3200, 800, 1500, 5000, 1200]}],
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_habit_tracker_components() -> list:
        """创建习惯追踪页面的组件列表"""
        template = PageTemplate(
            name="habit_tracker",
            display_name="习惯追踪",
            icon="checkmark",
            category="lifestyle",
            description="每日习惯养成和打卡",
        )

        template.add_component(TextBlockComponent(
            id="habit_tracker_title",
            content="习惯追踪",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="habit_tracker_desc",
            content="追踪每日习惯打卡，培养良好生活方式。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MetricCardComponent(
            id="habit_metrics",
            value="85",
            label="本周完成率",
            prefix="",
            suffix="%",
            trend="+10%",
            size="medium",
            order=3,
        ))

        template.add_component(TableComponent(
            id="habit_table",
            columns=[
                {"key": "habit", "title": "习惯", "width": "25%"},
                {"key": "goal", "title": "目标", "width": "15%"},
                {"key": "streak", "title": "连续天数", "width": "15%"},
                {"key": "total", "title": "总完成次数", "width": "20%"},
                {"key": "progress", "title": "完成率", "width": "25%"},
            ],
            data=[
                {"habit": "早起", "goal": "7:00 前起床", "streak": "5", "total": "15/30", "progress": "50%"},
                {"habit": "阅读", "goal": "30 分钟", "streak": "3", "total": "10/30", "progress": "33%"},
                {"habit": "运动", "goal": "20 分钟", "streak": "2", "total": "8/30", "progress": "27%"},
                {"habit": "冥想", "goal": "10 分钟", "streak": "7", "total": "20/30", "progress": "67%"},
                {"habit": "饮水", "goal": "8 杯水", "streak": "4", "total": "12/30", "progress": "40%"},
            ],
            order=4,
        ))

        template.add_component(ProgressBarComponent(
            id="habit_progress",
            percentage=43.0,
            style="circle",
            color="orange",
            order=5,
        ))

        template.add_component(CounterComponent(
            id="habit_counter",
            value=15,
            step=1,
            label="本月连续打卡天数",
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_event_checklist_components() -> list:
        """创建活动清单页面的组件列表"""
        template = PageTemplate(
            name="event_checklist",
            display_name="活动清单",
            icon="calendar",
            category="lifestyle",
            description="活动筹备和任务清单",
        )

        template.add_component(TextBlockComponent(
            id="event_checklist_title",
            content="活动清单",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="event_checklist_desc",
            content="筹备活动的完整任务清单，确保不遗漏任何事项。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(ListComponent(
            id="event_tasks",
            items=[
                {"label": "确定活动日期", "value": "task_1", "description": "确认参与者时间", "icon": "calendar", "checked": True},
                {"label": "预订场地", "value": "task_2", "description": "确认场地可用性", "icon": "home", "checked": True},
                {"label": "邀请嘉宾", "value": "task_3", "description": "发送邀请函", "icon": "mail", "checked": True},
                {"label": "准备物资", "value": "task_4", "description": "采购所需物品", "icon": "box", "checked": False},
                {"label": "布置场地", "value": "task_5", "description": "活动前一天布置", "icon": "tool", "checked": False},
                {"label": "活动彩排", "value": "task_6", "description": "确认流程和分工", "icon": "play", "checked": False},
                {"label": "活动执行", "value": "task_7", "description": "按计划执行", "icon": "flag", "checked": False},
                {"label": "活动总结", "value": "task_8", "description": "收集反馈并复盘", "icon": "file", "checked": False},
            ],
            list_type="simple",
            show_checkbox=True,
            order=3,
        ))

        template.add_component(StepsComponent(
            id="event_steps",
            steps=[
                {"id": "prepare", "title": "筹备阶段", "description": "确定方案", "status": "completed"},
                {"id": "ready", "title": "准备就绪", "description": "物资到位", "status": "in_progress"},
                {"id": "execute", "title": "执行活动", "description": "活动进行", "status": "pending"},
                {"id": "review", "title": "总结复盘", "description": "收集反馈", "status": "pending"},
            ],
            current=1,
            order=4,
        ))

        template.add_component(TimelineComponent(
            id="event_timeline",
            events=[
                {"id": "e_1", "title": "活动开始", "description": "签到入场", "date": "14:00", "icon": "clock"},
                {"id": "e_2", "title": "开场致辞", "description": "主持人致辞", "date": "14:30", "icon": "mic"},
                {"id": "e_3", "title": "主题活动", "description": "核心环节", "date": "15:00", "icon": "star"},
                {"id": "e_4", "title": "自由交流", "description": "茶歇互动", "date": "16:30", "icon": "chat"},
                {"id": "e_5", "title": "活动结束", "description": "合影留念", "date": "17:30", "icon": "camera"},
            ],
            layout="horizontal",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    # PAGE_TYPES 字典
    PAGE_TYPES = {
        "travel_board": {
            "name": "travel_board",
            "display_name": "旅行灵感板",
            "icon": "compass",
            "category": "lifestyle",
            "description": "旅行目的地灵感和规划",
            "default_schema": {
                "components": _create_travel_board_components.__func__(),
            }
        },
        "recipe_dev": {
            "name": "recipe_dev",
            "display_name": "食谱开发",
            "icon": "food",
            "category": "lifestyle",
            "description": "菜谱研发和配方管理",
            "default_schema": {
                "components": _create_recipe_dev_components.__func__(),
            }
        },
        "renovation_inspire": {
            "name": "renovation_inspire",
            "display_name": "装修灵感板",
            "icon": "home",
            "category": "lifestyle",
            "description": "家居装修灵感和规划",
            "default_schema": {
                "components": _create_renovation_inspire_components.__func__(),
            }
        },
        "fitness_plan": {
            "name": "fitness_plan",
            "display_name": "健身计划",
            "icon": "activity",
            "category": "lifestyle",
            "description": "训练计划和健身追踪",
            "default_schema": {
                "components": _create_fitness_plan_components.__func__(),
            }
        },
        "yearly_goals": {
            "name": "yearly_goals",
            "display_name": "年度目标",
            "icon": "target",
            "category": "lifestyle",
            "description": "年度目标和里程碑追踪",
            "default_schema": {
                "components": _create_yearly_goals_components.__func__(),
            }
        },
        "learning_roadmap": {
            "name": "learning_roadmap",
            "display_name": "学习路线图",
            "icon": "book",
            "category": "lifestyle",
            "description": "学习规划和技能路线图",
            "default_schema": {
                "components": _create_learning_roadmap_components.__func__(),
            }
        },
        "budget_plan": {
            "name": "budget_plan",
            "display_name": "预算计划",
            "icon": "wallet",
            "category": "lifestyle",
            "description": "个人收支预算管理",
            "default_schema": {
                "components": _create_budget_plan_components.__func__(),
            }
        },
        "habit_tracker": {
            "name": "habit_tracker",
            "display_name": "习惯追踪",
            "icon": "checkmark",
            "category": "lifestyle",
            "description": "每日习惯养成和打卡",
            "default_schema": {
                "components": _create_habit_tracker_components.__func__(),
            }
        },
        "event_checklist": {
            "name": "event_checklist",
            "display_name": "活动清单",
            "icon": "calendar",
            "category": "lifestyle",
            "description": "活动筹备和任务清单",
            "default_schema": {
                "components": _create_event_checklist_components.__func__(),
            }
        },
    }
