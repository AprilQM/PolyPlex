"""
设计领域页面模板 - 使用组件构建
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


class DesignPages:
    """设计领域页面模板"""

    @staticmethod
    def _create_moodboard_components() -> list:
        """创建情绪板页面的组件列表"""
        template = PageTemplate(
            name="moodboard",
            display_name="情绪板",
            icon="palette",
            category="design",
            description="收集灵感图片、色彩和参考素材",
        )

        template.add_component(TextBlockComponent(
            id="moodboard_title",
            content="情绪板",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="moodboard_desc",
            content="收集和整理设计灵感素材，包括色彩方案、图片参考和视觉方向。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MoodboardComponent(
            id="moodboard_canvas",
            items=[
                {"id": "item_1", "type": "image", "content": "灵感图片", "position": {"x": 0, "y": 0}},
                {"id": "item_2", "type": "color", "content": "#1890FF", "position": {"x": 200, "y": 0}},
                {"id": "item_3", "type": "text", "content": "设计方向参考", "position": {"x": 0, "y": 200}},
            ],
            order=3,
        ))

        template.add_component(ImageGalleryComponent(
            id="moodboard_images",
            images=[
                {"url": "", "caption": "参考图片 1", "alt": "design_reference_1"},
                {"url": "", "caption": "参考图片 2", "alt": "design_reference_2"},
                {"url": "", "caption": "参考图片 3", "alt": "design_reference_3"},
            ],
            layout="grid",
            columns=3,
            order=4,
        ))

        template.add_component(TagSetComponent(
            id="moodboard_tags",
            tags=[
                {"name": "灵感", "color": "blue", "count": 5},
                {"name": "色彩方案", "color": "green", "count": 3},
                {"name": "参考", "color": "orange", "count": 7},
            ],
            allow_create=True,
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_design_system_components() -> list:
        """创建设计系统页面的组件列表"""
        template = PageTemplate(
            name="design_system",
            display_name="设计系统",
            icon="grid",
            category="design",
            description="色彩、字体、间距等设计规范",
        )

        template.add_component(TextBlockComponent(
            id="design_system_title",
            content="设计系统",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="design_system_desc",
            content="项目设计规范和标准化指南，确保设计一致性。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="color_palette",
            columns=[
                {"key": "name", "title": "颜色名", "width": "20%"},
                {"key": "hex", "title": "色值", "width": "20%"},
                {"key": "usage", "title": "用途", "width": "45%"},
                {"key": "preview", "title": "预览", "width": "15%"},
            ],
            data=[
                {"name": "主色", "hex": "#1890FF", "usage": "主要操作按钮、链接", "preview": "blue"},
                {"name": "成功色", "hex": "#52C41A", "usage": "成功状态、完成", "preview": "green"},
                {"name": "警告色", "hex": "#FAAD14", "usage": "警告提示", "preview": "yellow"},
                {"name": "错误色", "hex": "#FF4D4F", "usage": "错误状态、删除", "preview": "red"},
            ],
            order=3,
        ))

        template.add_component(ListComponent(
            id="typography_specs",
            items=[
                {"label": "标题 1", "value": "h1", "description": "32px Bold - 页面大标题", "icon": "T"},
                {"label": "标题 2", "value": "h2", "description": "24px Bold - 区块标题", "icon": "T"},
                {"label": "标题 3", "value": "h3", "description": "20px Medium - 卡片标题", "icon": "T"},
                {"label": "正文", "value": "body", "description": "14px Regular - 正文内容", "icon": "T"},
                {"label": "小字", "value": "caption", "description": "12px Regular - 辅助文字", "icon": "T"},
            ],
            list_type="property",
            order=4,
        ))

        template.add_component(TagSetComponent(
            id="design_system_tags",
            tags=[
                {"name": "已完成", "color": "green", "count": 1},
                {"name": "进行中", "color": "blue", "count": 2},
                {"name": "待评审", "color": "orange", "count": 1},
            ],
            allow_create=True,
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_key_screens_components() -> list:
        """创建关键页面页面的组件列表"""
        template = PageTemplate(
            name="key_screens",
            display_name="关键页面",
            icon="image",
            category="design",
            description="核心界面设计稿展示",
        )

        template.add_component(TextBlockComponent(
            id="key_screens_title",
            content="关键页面设计",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="key_screens_desc",
            content="展示项目核心页面的设计稿，方便团队成员审阅和反馈。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(ImageGalleryComponent(
            id="screen_designs",
            images=[
                {"url": "", "caption": "首页设计稿 v2.0", "alt": "homepage_design"},
                {"url": "", "caption": "详情页设计稿 v1.5", "alt": "detail_design"},
                {"url": "", "caption": "个人中心设计稿 v1.0", "alt": "profile_design"},
                {"url": "", "caption": "设置页设计稿 v1.0", "alt": "settings_design"},
            ],
            layout="carousel",
            columns=2,
            order=3,
        ))

        template.add_component(CommentAnchorComponent(
            id="screen_comments",
            comments=[
                {"author": "设计师 A", "content": "首页布局需要调整间距", "time": "2024-01-15"},
            ],
            allow_comment=True,
            placeholder="输入对该页面的反馈意见...",
            order=4,
        ))

        template.add_component(ListComponent(
            id="screen_status",
            items=[
                {"label": "首页", "value": "done", "description": "已完成评审", "icon": "check", "checked": True},
                {"label": "详情页", "value": "review", "description": "待修改", "icon": "edit", "checked": False},
                {"label": "个人中心", "value": "draft", "description": "初稿完成", "icon": "file", "checked": False},
            ],
            list_type="simple",
            show_checkbox=True,
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_interaction_check_components() -> list:
        """创建交互走查页面的组件列表"""
        template = PageTemplate(
            name="interaction_check",
            display_name="交互走查",
            icon="list",
            category="design",
            description="交互细节和微动效检查清单",
        )

        template.add_component(TextBlockComponent(
            id="interaction_check_title",
            content="交互走查清单",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="interaction_check_desc",
            content="逐一检查交互细节，确保用户体验的一致性。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(ListComponent(
            id="interaction_items",
            items=[
                {"label": "按钮悬停状态", "value": "btn_hover", "description": "所有按钮悬停变色", "icon": "pointer", "checked": True},
                {"label": "页面过渡动画", "value": "transition", "description": "页面切换平滑过渡", "icon": "move", "checked": True},
                {"label": "加载状态", "value": "loading", "description": "数据加载时显示骨架屏", "icon": "refresh", "checked": False},
                {"label": "空状态展示", "value": "empty", "description": "无数据时显示占位图", "icon": "box", "checked": False},
                {"label": "错误反馈", "value": "error", "description": "操作失败时提示原因", "icon": "alert", "checked": True},
                {"label": "手势操作", "value": "gesture", "description": "移动端滑动返回支持", "icon": "hand", "checked": False},
            ],
            list_type="simple",
            show_checkbox=True,
            order=3,
        ))

        template.add_component(TableComponent(
            id="interaction_issues",
            columns=[
                {"key": "module", "title": "模块", "width": "20%"},
                {"key": "issue", "title": "问题描述", "width": "40%"},
                {"key": "priority", "title": "优先级", "width": "20%"},
                {"key": "status", "title": "状态", "width": "20%"},
            ],
            data=[
                {"module": "导航", "issue": "返回按钮缺少按压态", "priority": "高", "status": "已修复"},
                {"module": "表单", "issue": "输入框聚焦动画不连贯", "priority": "中", "status": "处理中"},
            ],
            order=4,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_journey_map_components() -> list:
        """创建用户旅程地图页面的组件列表"""
        template = PageTemplate(
            name="journey_map",
            display_name="用户旅程",
            icon="map",
            category="design",
            description="用户旅程地图和体验分析",
        )

        template.add_component(TextBlockComponent(
            id="journey_map_title",
            content="用户旅程地图",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="journey_map_desc",
            content="绘制用户在使用产品过程中的完整旅程，识别痛点和优化机会。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TimelineComponent(
            id="journey_timeline",
            events=[
                {"id": "step_1", "title": "发现", "description": "用户通过搜索找到产品", "date": "阶段 1", "icon": "search"},
                {"id": "step_2", "title": "了解", "description": "浏览产品介绍和功能", "date": "阶段 1", "icon": "eye"},
                {"id": "step_3", "title": "注册", "description": "创建账号并完善资料", "date": "阶段 2", "icon": "user"},
                {"id": "step_4", "title": "使用", "description": "体验核心功能", "date": "阶段 2", "icon": "play"},
                {"id": "step_5", "title": "留存", "description": "形成使用习惯", "date": "阶段 3", "icon": "heart"},
            ],
            layout="horizontal",
            order=3,
        ))

        template.add_component(FlowchartComponent(
            id="journey_flow",
            nodes=[
                {"id": "start", "label": "用户进入", "type": "start"},
                {"id": "search", "label": "搜索产品", "type": "action"},
                {"id": "landing", "label": "访问首页", "type": "page"},
                {"id": "register", "label": "注册账号", "type": "action"},
                {"id": "onboarding", "label": "新手引导", "type": "page"},
                {"id": "core", "label": "使用核心功能", "type": "action"},
                {"id": "end", "label": "离开", "type": "end"},
            ],
            edges=[
                {"source": "start", "target": "search", "label": ""},
                {"source": "search", "target": "landing", "label": "点击结果"},
                {"source": "landing", "target": "register", "label": "点击注册"},
                {"source": "register", "target": "onboarding", "label": "注册成功"},
                {"source": "onboarding", "target": "core", "label": "跳过引导"},
                {"source": "core", "target": "end", "label": ""},
            ],
            order=4,
        ))

        template.add_component(RelationGraphComponent(
            id="journey_relations",
            nodes=[
                {"id": "user", "label": "用户", "group": "persona"},
                {"id": "product", "label": "产品", "group": "system"},
                {"id": "service", "label": "客服", "group": "system"},
                {"id": "content", "label": "内容", "group": "resource"},
            ],
            edges=[
                {"source": "user", "target": "product", "label": "使用"},
                {"source": "user", "target": "service", "label": "咨询"},
                {"source": "product", "target": "content", "label": "提供"},
            ],
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_info_arch_components() -> list:
        """创建信息架构页面的组件列表"""
        template = PageTemplate(
            name="info_arch",
            display_name="信息架构",
            icon="sitemap",
            category="design",
            description="站点地图和信息层级结构",
        )

        template.add_component(TextBlockComponent(
            id="info_arch_title",
            content="信息架构",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="info_arch_desc",
            content="定义产品的信息层级、导航结构和内容组织方式。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MindmapComponent(
            id="site_mindmap",
            nodes=[
                {"id": "root", "label": "产品", "children": ["nav", "content", "user"], "parent": None},
                {"id": "nav", "label": "导航", "children": ["home", "explore", "search"], "parent": "root"},
                {"id": "content", "label": "内容", "children": ["detail", "list", "article"], "parent": "root"},
                {"id": "user", "label": "用户", "children": ["profile", "settings", "help"], "parent": "root"},
                {"id": "home", "label": "首页", "children": [], "parent": "nav"},
                {"id": "explore", "label": "发现", "children": [], "parent": "nav"},
                {"id": "search", "label": "搜索", "children": [], "parent": "nav"},
                {"id": "detail", "label": "详情页", "children": [], "parent": "content"},
                {"id": "list", "label": "列表页", "children": [], "parent": "content"},
                {"id": "article", "label": "文章页", "children": [], "parent": "content"},
                {"id": "profile", "label": "个人中心", "children": [], "parent": "user"},
                {"id": "settings", "label": "设置", "children": [], "parent": "user"},
                {"id": "help", "label": "帮助中心", "children": [], "parent": "user"},
            ],
            layout="tree",
            order=3,
        ))

        template.add_component(ListComponent(
            id="ia_notes",
            items=[
                {"label": "首页", "value": "home", "description": "展示推荐内容和核心入口", "icon": "home"},
                {"label": "发现页", "value": "explore", "description": "分类浏览和搜索入口", "icon": "compass"},
                {"label": "详情页", "value": "detail", "description": "展示完整信息", "icon": "file"},
                {"label": "个人中心", "value": "profile", "description": "用户信息和设置入口", "icon": "user"},
            ],
            list_type="definition",
            order=4,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_usability_test_components() -> list:
        """创建可用性测试页面的组件列表"""
        template = PageTemplate(
            name="usability_test",
            display_name="可用性测试",
            icon="clipboard",
            category="design",
            description="可用性测试计划与结果分析",
        )

        template.add_component(TextBlockComponent(
            id="usability_test_title",
            content="可用性测试",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="usability_test_desc",
            content="制定可用性测试计划，记录测试过程和结果分析。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(StepsComponent(
            id="test_steps",
            steps=[
                {"id": "step_1", "title": "制定计划", "description": "确定测试目标和范围", "status": "completed"},
                {"id": "step_2", "title": "招募用户", "description": "招募符合条件的目标用户", "status": "completed"},
                {"id": "step_3", "title": "执行测试", "description": "按计划执行可用性测试", "status": "in_progress"},
                {"id": "step_4", "title": "分析结果", "description": "整理测试数据和发现问题", "status": "pending"},
                {"id": "step_5", "title": "输出报告", "description": "撰写可用性测试报告", "status": "pending"},
            ],
            current=2,
            order=3,
        ))

        template.add_component(TableComponent(
            id="test_results",
            columns=[
                {"key": "task", "title": "测试任务", "width": "25%"},
                {"key": "success_rate", "title": "完成率", "width": "15%"},
                {"key": "avg_time", "title": "平均用时", "width": "15%"},
                {"key": "issues", "title": "发现问题", "width": "30%"},
                {"key": "severity", "title": "严重程度", "width": "15%"},
            ],
            data=[
                {"task": "注册流程", "success_rate": "85%", "avg_time": "120s", "issues": "验证码输入不便", "severity": "中"},
                {"task": "发布内容", "success_rate": "70%", "avg_time": "180s", "issues": "步骤过多", "severity": "高"},
                {"task": "查找信息", "success_rate": "90%", "avg_time": "45s", "issues": "筛选不够直观", "severity": "低"},
            ],
            order=4,
        ))

        template.add_component(ScorecardComponent(
            id="usability_score",
            dimensions=[
                {"name": "效率", "weight": 30, "max_score": 100, "score": 75},
                {"name": "满意度", "weight": 25, "max_score": 100, "score": 80},
                {"name": "易学性", "weight": 25, "max_score": 100, "score": 70},
                {"name": "容错性", "weight": 20, "max_score": 100, "score": 65},
            ],
            score_type="star",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_design_review_components() -> list:
        """创建设计评审页面的组件列表"""
        template = PageTemplate(
            name="design_review",
            display_name="设计评审",
            icon="checklist",
            category="design",
            description="设计稿评审与反馈记录",
        )

        template.add_component(TextBlockComponent(
            id="design_review_title",
            content="设计评审",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="design_review_desc",
            content="组织和记录设计评审活动，收集反馈并追踪修改。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="review_items",
            columns=[
                {"key": "page", "title": "页面", "width": "20%"},
                {"key": "reviewer", "title": "评审人", "width": "15%"},
                {"key": "feedback", "title": "反馈意见", "width": "35%"},
                {"key": "priority", "title": "优先级", "width": "15%"},
                {"key": "status", "title": "状态", "width": "15%"},
            ],
            data=[
                {"page": "首页", "reviewer": "产品经理", "feedback": "建议增加引导提示", "priority": "高", "status": "已修改"},
                {"page": "详情页", "reviewer": "开发", "feedback": "图片懒加载需优化", "priority": "中", "status": "处理中"},
                {"page": "设置页", "reviewer": "设计师 B", "feedback": "间距不统一", "priority": "低", "status": "待处理"},
            ],
            order=3,
        ))

        template.add_component(VoteModuleComponent(
            id="review_vote",
            question="是否通过本轮评审？",
            options=[
                {"text": "通过", "count": 5},
                {"text": "有条件通过", "count": 3},
                {"text": "不通过，需修改", "count": 1},
            ],
            vote_type="single",
            order=4,
        ))

        template.add_component(CommentAnchorComponent(
            id="review_comments",
            comments=[
                {"author": "设计师 A", "content": "首页的配色方案需要调整", "time": "2024-01-20"},
                {"author": "产品经理", "content": "详情页的信息层级建议优化", "time": "2024-01-21"},
            ],
            allow_comment=True,
            placeholder="输入评审意见...",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    # PAGE_TYPES 字典
    PAGE_TYPES = {
        "moodboard": {
            "name": "moodboard",
            "display_name": "情绪板",
            "icon": "palette",
            "category": "design",
            "description": "收集灵感图片、色彩和参考素材",
            "default_schema": {
                "components": _create_moodboard_components.__func__(),
            }
        },
        "design_system": {
            "name": "design_system",
            "display_name": "设计系统",
            "icon": "grid",
            "category": "design",
            "description": "色彩、字体、间距等设计规范",
            "default_schema": {
                "components": _create_design_system_components.__func__(),
            }
        },
        "key_screens": {
            "name": "key_screens",
            "display_name": "关键页面",
            "icon": "image",
            "category": "design",
            "description": "核心界面设计稿展示",
            "default_schema": {
                "components": _create_key_screens_components.__func__(),
            }
        },
        "interaction_check": {
            "name": "interaction_check",
            "display_name": "交互走查",
            "icon": "list",
            "category": "design",
            "description": "交互细节和微动效检查清单",
            "default_schema": {
                "components": _create_interaction_check_components.__func__(),
            }
        },
        "journey_map": {
            "name": "journey_map",
            "display_name": "用户旅程",
            "icon": "map",
            "category": "design",
            "description": "用户旅程地图和体验分析",
            "default_schema": {
                "components": _create_journey_map_components.__func__(),
            }
        },
        "info_arch": {
            "name": "info_arch",
            "display_name": "信息架构",
            "icon": "sitemap",
            "category": "design",
            "description": "站点地图和信息层级结构",
            "default_schema": {
                "components": _create_info_arch_components.__func__(),
            }
        },
        "usability_test": {
            "name": "usability_test",
            "display_name": "可用性测试",
            "icon": "clipboard",
            "category": "design",
            "description": "可用性测试计划与结果分析",
            "default_schema": {
                "components": _create_usability_test_components.__func__(),
            }
        },
        "design_review": {
            "name": "design_review",
            "display_name": "设计评审",
            "icon": "checklist",
            "category": "design",
            "description": "设计稿评审与反馈记录",
            "default_schema": {
                "components": _create_design_review_components.__func__(),
            }
        },
    }
