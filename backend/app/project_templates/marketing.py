"""
营销领域页面模板 - 内容日历、社媒排期、活动方案、素材看板、漏斗分析、品牌画布
"""
from app.page_components import (
    PageTemplate,
    TextBlockComponent, TableComponent, ListComponent, KanbanComponent, TabsComponent, StepsComponent,
    DataChartComponent, DividerComponent, SpacerComponent,
    ContentCalendarComponent, FunnelComponent,
)


class MarketingPages:
    """营销领域页面模板"""

    @staticmethod
    def _create_content_calendar_components() -> list:
        template = PageTemplate(name="content_calendar", display_name="内容日历", icon="calendar", category="marketing", description="内容发布计划与排期")
        template.add_component(TextBlockComponent(id="title", content="内容日历", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="规划和管理内容创作与发布日程。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(ContentCalendarComponent(
            id="calendar",
            items=[
                {"title": "新品发布文章", "type": "blog", "channel": "官网", "status": "planned", "assignee": "张三", "publish_date": "2026-05-10"},
                {"title": "产品介绍视频", "type": "video", "channel": "YouTube", "status": "in_progress", "assignee": "李四", "publish_date": "2026-05-15"},
                {"title": "促销活动推文", "type": "social", "channel": "微博", "status": "planned", "assignee": "王五", "publish_date": "2026-05-20"},
            ],
            view="calendar",
            order=3,
        ))
        template.add_component(TextBlockComponent(id="calendar_notes", content="排期说明：标注重点日期和内容策略。", sub_type="paragraph", placeholder="节假日营销节点、内容主题规划、跨渠道协调", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_social_schedule_components() -> list:
        template = PageTemplate(name="social_schedule", display_name="社媒排期", icon="share-2", category="marketing", description="社交媒体发布排期")
        template.add_component(TextBlockComponent(id="title", content="社媒排期", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="管理各社交媒体平台的发布排期。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TableComponent(
            id="schedule_table",
            columns=[
                {"key": "date", "title": "日期", "width": "12%"},
                {"key": "platform", "title": "平台", "width": "12%"},
                {"key": "content", "title": "内容", "width": "30%"},
                {"key": "format", "title": "格式", "width": "12%"},
                {"key": "status", "title": "状态", "width": "14%"},
                {"key": "engagement", "title": "预期互动", "width": "20%"},
            ],
            data=[
                {"date": "05-10", "platform": "微信公众号", "content": "行业趋势分析", "format": "图文", "status": "已排期", "engagement": "阅读量目标"},
                {"date": "05-12", "platform": "小红书", "content": "产品使用教程", "format": "短视频", "status": "制作中", "engagement": "点赞目标"},
                {"date": "05-14", "platform": "LinkedIn", "content": "公司动态更新", "format": "图文", "status": "已排期", "engagement": "互动目标"},
            ],
            order=3,
        ))
        template.add_component(ListComponent(
            id="platform_strategy",
            items=[
                {"label": "微信策略", "value": "wechat", "description": "深度内容，每周2篇"},
                {"label": "小红书策略", "value": "redbook", "description": "种草笔记，每日1篇"},
                {"label": "微博策略", "value": "weibo", "description": "热点话题，实时更新"},
            ],
            list_type="definition",
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_campaign_plan_components() -> list:
        template = PageTemplate(name="campaign_plan", display_name="活动方案", icon="megaphone", category="marketing", description="营销活动策划方案")
        template.add_component(TextBlockComponent(id="title", content="活动方案", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="策划完整的营销活动方案和执行计划。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TabsComponent(
            id="campaign_tabs",
            tabs=[
                {"key": "overview", "label": "活动概览", "icon": "info", "content": [{"type": "text_block", "data": {"content": "活动目标、预算、时间线等概要信息", "sub_type": "paragraph"}}]},
                {"key": "timeline", "label": "执行时间线", "icon": "clock", "content": [{"type": "text_block", "data": {"content": "各阶段执行节点和里程碑", "sub_type": "paragraph"}}]},
                {"key": "budget", "label": "预算分配", "icon": "dollar-sign", "content": [{"type": "text_block", "data": {"content": "各渠道预算分配和ROI预估", "sub_type": "paragraph"}}]},
            ],
            tab_position="top",
            order=3,
        ))
        template.add_component(StepsComponent(
            id="campaign_steps",
            steps=[
                {"id": "planning", "title": "策划阶段", "description": "目标设定与策略制定", "status": "completed"},
                {"id": "preparation", "title": "准备阶段", "description": "物料设计与资源协调", "status": "in_progress"},
                {"id": "launch", "title": "上线执行", "description": "活动正式发布", "status": "pending"},
                {"id": "review", "title": "复盘总结", "description": "数据分析与效果评估", "status": "pending"},
            ],
            current=1,
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_asset_board_components() -> list:
        template = PageTemplate(name="asset_board", display_name="素材看板", icon="layout", category="marketing", description="营销素材管理看板")
        template.add_component(TextBlockComponent(id="title", content="素材看板", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="管理和跟踪营销素材的制作进度。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(KanbanComponent(
            id="asset_kanban",
            columns=[
                {"id": "todo", "title": "待制作", "color": "#E8E8E8"},
                {"id": "in_progress", "title": "制作中", "color": "#BAE7FF"},
                {"id": "review", "title": "审核中", "color": "#FFE58F"},
                {"id": "done", "title": "已完成", "color": "#B7EB8F"},
            ],
            cards=[
                {"id": "card1", "title": "主视觉海报", "description": "活动主KV设计", "column_id": "in_progress", "priority": "high", "assignee": "设计师A", "due_date": "2026-05-12"},
                {"id": "card2", "title": "产品介绍页", "description": "落地页文案", "column_id": "todo", "priority": "medium", "assignee": "文案B", "due_date": "2026-05-15"},
                {"id": "card3", "title": "社交媒体 banner", "description": "各平台适配图", "column_id": "review", "priority": "high", "assignee": "设计师A", "due_date": "2026-05-10"},
            ],
            order=3,
        ))
        template.add_component(TextBlockComponent(id="asset_notes", content="素材说明：记录规格要求和品牌规范。", sub_type="paragraph", placeholder="尺寸规格、品牌色彩、字体要求、输出格式", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_funnel_analysis_components() -> list:
        template = PageTemplate(name="funnel_analysis", display_name="漏斗分析", icon="funnel", category="marketing", description="营销转化漏斗分析")
        template.add_component(TextBlockComponent(id="title", content="漏斗分析", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="分析各环节转化率和优化机会。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(FunnelComponent(
            id="funnel",
            stages=[
                {"name": "曝光", "count": 10000, "conversion_rate": 100.0},
                {"name": "点击", "count": 2500, "conversion_rate": 25.0},
                {"name": "注册", "count": 800, "conversion_rate": 8.0},
                {"name": "下单", "count": 200, "conversion_rate": 2.0},
                {"name": "复购", "count": 60, "conversion_rate": 0.6},
            ],
            order=3,
        ))
        template.add_component(DataChartComponent(
            id="funnel_chart",
            chart_type="bar",
            labels=["曝光", "点击", "注册", "下单", "复购"],
            datasets=[{"label": "用户数", "data": [10000, 2500, 800, 200, 60]}],
            order=4,
        ))
        template.add_component(TextBlockComponent(id="optimization", content="优化建议：分析瓶颈环节和提升策略。", sub_type="paragraph", placeholder="各环节流失原因分析、AB测试计划、优化优先级", order=5))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_brand_canvas_components() -> list:
        template = PageTemplate(name="brand_canvas", display_name="品牌画布", icon="target", category="marketing", description="品牌定位与策略画布")
        template.add_component(TextBlockComponent(id="title", content="品牌画布", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="定义品牌定位、核心价值和传播策略。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TextBlockComponent(id="brand_statement", content="品牌定位声明：描述品牌核心价值和目标受众。", sub_type="alert", placeholder="品牌标识语、核心定位、目标人群描述", order=3))
        template.add_component(ListComponent(
            id="brand_elements",
            items=[
                {"label": "品牌使命", "value": "mission", "description": "品牌存在的社会价值"},
                {"label": "品牌愿景", "value": "vision", "description": "品牌长期发展目标"},
                {"label": "品牌个性", "value": "personality", "description": "品牌拟人化特征"},
                {"label": "目标受众", "value": "audience", "description": "核心用户画像"},
                {"label": "差异化优势", "value": "differentiator", "description": "与竞品的核心差异"},
            ],
            list_type="property",
            order=4,
        ))
        template.add_component(TableComponent(
            id="brand_channels",
            columns=[
                {"key": "channel", "title": "渠道", "width": "20%"},
                {"key": "tone", "title": "语气风格", "width": "25%"},
                {"key": "content_type", "title": "内容类型", "width": "30%"},
                {"key": "frequency", "title": "发布频率", "width": "25%"},
            ],
            data=[
                {"channel": "官网", "tone": "专业权威", "content_type": "深度文章", "frequency": "每周2篇"},
                {"channel": "社交媒体", "tone": "亲切活泼", "content_type": "短视频", "frequency": "每日发布"},
            ],
            order=5,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    PAGE_TYPES = {
        "content_calendar": {
            "name": "content_calendar", "display_name": "内容日历", "icon": "calendar",
            "category": "marketing", "description": "内容发布计划与排期",
            "default_schema": {"entries": [], "components": _create_content_calendar_components.__func__()}
        },
        "social_schedule": {
            "name": "social_schedule", "display_name": "社媒排期", "icon": "share-2",
            "category": "marketing", "description": "社交媒体发布排期",
            "default_schema": {"posts": [], "components": _create_social_schedule_components.__func__()}
        },
        "campaign_plan": {
            "name": "campaign_plan", "display_name": "活动方案", "icon": "megaphone",
            "category": "marketing", "description": "营销活动策划方案",
            "default_schema": {"campaign": {}, "components": _create_campaign_plan_components.__func__()}
        },
        "asset_board": {
            "name": "asset_board", "display_name": "素材看板", "icon": "layout",
            "category": "marketing", "description": "营销素材管理看板",
            "default_schema": {"assets": [], "components": _create_asset_board_components.__func__()}
        },
        "funnel_analysis": {
            "name": "funnel_analysis", "display_name": "漏斗分析", "icon": "funnel",
            "category": "marketing", "description": "营销转化漏斗分析",
            "default_schema": {"stages": [], "components": _create_funnel_analysis_components.__func__()}
        },
        "brand_canvas": {
            "name": "brand_canvas", "display_name": "品牌画布", "icon": "target",
            "category": "marketing", "description": "品牌定位与策略画布",
            "default_schema": {"brand": {}, "components": _create_brand_canvas_components.__func__()}
        },
    }
