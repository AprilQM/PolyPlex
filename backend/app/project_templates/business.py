"""
商业领域页面模板 - 使用新组件系统构建
包含11种商业页面类型：精益画布、商业模式画布、用户画像、竞品分析矩阵、SWOT分析、
市场简报、商业计划书大纲、定价策略、渠道策略、路演PPT、收入模型
"""

from app.page_components import (
    PageTemplate,
    TextBlockComponent,
    DividerComponent,
    SpacerComponent,
    TableComponent,
    ListComponent,
    StepsComponent,
    MetricCardComponent,
    BizCanvasComponent,
    PersonaCardComponent,
    SwotComponent,
    CompeteMatrixComponent,
)


class BusinessPages:
    """商业领域页面模板 - 11种页面类型"""

    @staticmethod
    def _create_lean_canvas_components() -> list:
        """创建精益画布页面的组件列表"""
        template = PageTemplate(
            name="lean_canvas",
            display_name="精益画布",
            icon="grid",
            category="business",
            description="精益画布九宫格，用于快速梳理商业模式假设",
        )

        template.add_component(TextBlockComponent(
            id="lean_canvas_title",
            content="精益画布",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="lean_canvas_desc",
            content="使用精益画布快速梳理商业模式的核心假设，包括问题、解决方案、关键指标、独特卖点等九个维度。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(BizCanvasComponent(
            id="lean_canvas_board",
            template="lean_canvas",
            cells={},
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_biz_model_canvas_components() -> list:
        """创建商业模式画布页面的组件列表"""
        template = PageTemplate(
            name="biz_model_canvas",
            display_name="商业模式画布",
            icon="grid",
            category="business",
            description="经典商业模式画布九宫格，分析商业模式的九大构建模块",
        )

        template.add_component(TextBlockComponent(
            id="biz_model_canvas_title",
            content="商业模式画布",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="biz_model_canvas_desc",
            content="使用商业模式画布系统分析价值主张、客户细分、渠道通路、客户关系、收入来源、核心资源、关键业务、重要伙伴和成本结构。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(BizCanvasComponent(
            id="biz_model_canvas_board",
            template="business_model",
            cells={},
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_user_persona_components() -> list:
        """创建用户画像页面的组件列表"""
        template = PageTemplate(
            name="user_persona",
            display_name="用户画像",
            icon="users",
            category="business",
            description="目标用户特征描述与画像卡片",
        )

        template.add_component(TextBlockComponent(
            id="user_persona_title",
            content="用户画像",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="user_persona_desc",
            content="描述目标用户的特征、需求、痛点和行为模式，帮助团队建立对用户的统一认知。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(PersonaCardComponent(
            id="persona_primary",
            name="典型用户",
            demographics={
                "age": "25-40",
                "occupation": "产品经理/创业者",
                "location": "一线城市",
                "education": "本科及以上",
            },
            goals=["提升工作效率", "降低沟通成本"],
            pain_points=["信息分散", "协作效率低"],
            behaviors=["每天使用办公软件", "关注行业动态"],
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_compete_matrix_components() -> list:
        """创建竞品分析矩阵页面的组件列表"""
        template = PageTemplate(
            name="compete_matrix",
            display_name="竞品分析矩阵",
            icon="matrix",
            category="business",
            description="多维度竞品对比分析矩阵",
        )

        template.add_component(TextBlockComponent(
            id="compete_matrix_title",
            content="竞品分析矩阵",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="compete_matrix_desc",
            content="从多个维度对比分析竞品，识别市场竞争格局和差异化机会。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(CompeteMatrixComponent(
            id="compete_matrix_board",
            competitors=["竞品A", "竞品B", "竞品C"],
            dimensions=["功能完整度", "用户体验", "价格优势", "市场份额", "技术实力"],
            scores={},
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_swot_components() -> list:
        """创建SWOT分析页面的组件列表"""
        template = PageTemplate(
            name="swot",
            display_name="SWOT分析",
            icon="chart",
            category="business",
            description="优势、劣势、机会、威胁四象限分析",
        )

        template.add_component(TextBlockComponent(
            id="swot_title",
            content="SWOT分析",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="swot_desc",
            content="通过分析内部优势与劣势、外部机会与威胁，制定有效的业务策略。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(SwotComponent(
            id="swot_board",
            strengths=["品牌知名度高", "技术团队实力强", "现有客户基础稳定"],
            weaknesses=["市场覆盖范围有限", "产品线单一", "资金储备不足"],
            opportunities=["新兴市场需求增长", "政策利好", "技术变革窗口期"],
            threats=["竞争对手快速扩张", "替代品出现", "监管趋严"],
            strategies={},
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_market_brief_components() -> list:
        """创建市场简报页面的组件列表"""
        template = PageTemplate(
            name="market_brief",
            display_name="市场简报",
            icon="briefcase",
            category="business",
            description="市场调研数据与分析简报",
        )

        template.add_component(TextBlockComponent(
            id="market_brief_title",
            content="市场简报",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="market_brief_desc",
            content="汇总市场调研关键数据，快速了解市场格局、趋势和竞争环境。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MetricCardComponent(
            id="market_size",
            value="500",
            label="市场规模（亿元）",
            prefix="",
            suffix="亿",
            trend="up",
            size="medium",
            order=3,
        ))

        template.add_component(MetricCardComponent(
            id="growth_rate",
            value="15",
            label="年增长率",
            prefix="",
            suffix="%",
            trend="up",
            size="medium",
            order=4,
        ))

        template.add_component(MetricCardComponent(
            id="market_share",
            value="8",
            label="市场份额",
            prefix="",
            suffix="%",
            trend=None,
            size="medium",
            order=5,
        ))

        template.add_component(DividerComponent(order=6))

        template.add_component(TableComponent(
            id="market_segments",
            title="细分市场数据",
            columns=[
                {"key": "segment", "title": "细分市场", "width": "25%"},
                {"key": "size", "title": "规模（亿元）", "width": "20%"},
                {"key": "growth", "title": "增长率", "width": "20%"},
                {"key": "competitors", "title": "主要竞争者", "width": "20%"},
                {"key": "maturity", "title": "成熟度", "width": "15%"},
            ],
            data=[
                {"segment": "高端市场", "size": "200", "growth": "10%", "competitors": "A公司、B公司", "maturity": "成熟"},
                {"segment": "中端市场", "size": "200", "growth": "18%", "competitors": "C公司、D公司", "maturity": "成长"},
                {"segment": "低端市场", "size": "100", "growth": "25%", "competitors": "E公司、F公司", "maturity": "新兴"},
            ],
            order=7,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_biz_plan_outline_components() -> list:
        """创建商业计划书大纲页面的组件列表"""
        template = PageTemplate(
            name="biz_plan_outline",
            display_name="商业计划书大纲",
            icon="document",
            category="business",
            description="商业计划书章节结构与步骤指引",
        )

        template.add_component(TextBlockComponent(
            id="biz_plan_outline_title",
            content="商业计划书大纲",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="biz_plan_outline_desc",
            content="商业计划书的章节结构和编写步骤，按顺序完成各部分的撰写。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(StepsComponent(
            id="plan_steps",
            steps=[
                {"id": "exec_summary", "title": "执行摘要", "description": "项目概述、核心亮点与投资诉求", "status": "pending"},
                {"id": "company_desc", "title": "公司描述", "description": "公司愿景、使命与发展历程", "status": "pending"},
                {"id": "market_analysis", "title": "市场分析", "description": "市场规模、趋势与竞争格局", "status": "pending"},
                {"id": "product_service", "title": "产品与服务", "description": "产品功能、技术与知识产权", "status": "pending"},
                {"id": "marketing_sales", "title": "营销策略", "description": "推广渠道、销售策略与定价", "status": "pending"},
                {"id": "financial_proj", "title": "财务预测", "description": "收入预测、成本分析与盈亏平衡", "status": "pending"},
            ],
            current=0,
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_pricing_strategy_components() -> list:
        """创建定价策略页面的组件列表"""
        template = PageTemplate(
            name="pricing_strategy",
            display_name="定价策略",
            icon="tag",
            category="business",
            description="产品定价策略与价格体系设计",
        )

        template.add_component(TextBlockComponent(
            id="pricing_strategy_title",
            content="定价策略",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="pricing_strategy_desc",
            content="设计产品的定价策略，包括价格档位、付费模式和定价依据。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="pricing_tiers",
            title="价格体系",
            columns=[
                {"key": "tier", "title": "档位", "width": "15%"},
                {"key": "price", "title": "价格", "width": "15%"},
                {"key": "features", "title": "核心功能", "width": "35%"},
                {"key": "target", "title": "目标用户", "width": "20%"},
                {"key": "notes", "title": "备注", "width": "15%"},
            ],
            data=[
                {"tier": "免费版", "price": "￥0", "features": "基础功能, 有限存储", "target": "个人用户", "notes": "引流"},
                {"tier": "专业版", "price": "￥99/月", "features": "全部功能, 高级分析", "target": "中小企业", "notes": "主力产品"},
                {"tier": "企业版", "price": "￥499/月", "features": "定制功能, API接入, 专属支持", "target": "大型企业", "notes": "高利润"},
            ],
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_channel_strategy_components() -> list:
        """创建渠道策略页面的组件列表"""
        template = PageTemplate(
            name="channel_strategy",
            display_name="渠道策略",
            icon="share",
            category="business",
            description="市场推广与销售渠道策略规划",
        )

        template.add_component(TextBlockComponent(
            id="channel_strategy_title",
            content="渠道策略",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="channel_strategy_desc",
            content="规划市场推广和销售渠道策略，明确各个渠道的目标、资源和考核指标。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(ListComponent(
            id="channel_list",
            title="渠道规划",
            items=[
                {"label": "线上推广", "value": "online", "description": "搜索引擎广告、社交媒体营销、内容营销"},
                {"label": "线下渠道", "value": "offline", "description": "行业展会、地推团队、渠道合作伙伴"},
                {"label": "直销团队", "value": "direct", "description": "电话销售、客户拜访、产品演示"},
                {"label": "渠道合作", "value": "partner", "description": "代理商体系、集成商合作、联盟营销"},
            ],
            list_type="definition",
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_pitch_deck_components() -> list:
        """创建路演PPT页面的组件列表"""
        template = PageTemplate(
            name="pitch_deck",
            display_name="路演PPT",
            icon="presentation",
            category="business",
            description="项目路演演示文稿大纲与内容",
        )

        template.add_component(TextBlockComponent(
            id="pitch_deck_title",
            content="路演PPT",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="pitch_deck_desc",
            content="项目路演演示文稿的内容大纲和结构设计，用于向投资人展示项目价值。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(ListComponent(
            id="deck_sections",
            title="路演结构",
            items=[
                {"label": "封面与愿景", "value": "slide_1", "description": "项目名称、公司Logo、一句话愿景"},
                {"label": "问题与痛点", "value": "slide_2", "description": "目标用户面临的核心问题"},
                {"label": "解决方案", "value": "slide_3", "description": "产品/服务的核心价值主张"},
                {"label": "市场机会", "value": "slide_4", "description": "市场规模、增长趋势与目标客户"},
                {"label": "商业模式", "value": "slide_5", "description": "收入来源与盈利模式"},
                {"label": "竞争分析", "value": "slide_6", "description": "竞争优势与差异化策略"},
                {"label": "团队介绍", "value": "slide_7", "description": "核心团队背景与优势"},
                {"label": "财务预测", "value": "slide_8", "description": "营收预测与融资需求"},
            ],
            list_type="definition",
            order=3,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_revenue_model_components() -> list:
        """创建收入模型页面的组件列表"""
        template = PageTemplate(
            name="revenue_model",
            display_name="收入模型",
            icon="chart",
            category="business",
            description="收入来源分析与盈利模式设计",
        )

        template.add_component(TextBlockComponent(
            id="revenue_model_title",
            content="收入模型",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="revenue_model_desc",
            content="分析收入来源结构，设计可持续的盈利模式，预测财务表现。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MetricCardComponent(
            id="total_revenue",
            value="1000",
            label="预计年收入（万元）",
            prefix="￥",
            suffix="万",
            trend="up",
            size="medium",
            order=3,
        ))

        template.add_component(MetricCardComponent(
            id="profit_margin",
            value="35",
            label="毛利率",
            prefix="",
            suffix="%",
            trend="up",
            size="medium",
            order=4,
        ))

        template.add_component(DividerComponent(order=5))

        template.add_component(TableComponent(
            id="revenue_streams",
            title="收入来源明细",
            columns=[
                {"key": "stream", "title": "收入来源", "width": "20%"},
                {"key": "description", "title": "说明", "width": "30%"},
                {"key": "percentage", "title": "占比", "width": "15%"},
                {"key": "growth", "title": "增长趋势", "width": "15%"},
                {"key": "notes", "title": "备注", "width": "20%"},
            ],
            data=[
                {"stream": "订阅收入", "description": "用户按月/年付费", "percentage": "60%", "growth": "稳定增长", "notes": "核心收入"},
                {"stream": "增值服务", "description": "按需付费功能", "percentage": "20%", "growth": "快速增长", "notes": "高利润"},
                {"stream": "广告收入", "description": "平台广告展示", "percentage": "10%", "growth": "稳步增长", "notes": "流量变现"},
                {"stream": "企业服务", "description": "定制化方案", "percentage": "10%", "growth": "快速增长", "notes": "新业务线"},
            ],
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # PAGE_TYPES 字典
    PAGE_TYPES = {
        "lean_canvas": {
            "name": "lean_canvas",
            "display_name": "精益画布",
            "icon": "grid",
            "category": "business",
            "description": "精益画布九宫格，用于快速梳理商业模式假设",
            "default_schema": {
                "cells": {},
                "components": _create_lean_canvas_components.__func__(),
            }
        },
        "biz_model_canvas": {
            "name": "biz_model_canvas",
            "display_name": "商业模式画布",
            "icon": "grid",
            "category": "business",
            "description": "经典商业模式画布九宫格，分析商业模式的九大构建模块",
            "default_schema": {
                "cells": {},
                "components": _create_biz_model_canvas_components.__func__(),
            }
        },
        "user_persona": {
            "name": "user_persona",
            "display_name": "用户画像",
            "icon": "users",
            "category": "business",
            "description": "目标用户特征描述与画像卡片",
            "default_schema": {
                "personas": [],
                "components": _create_user_persona_components.__func__(),
            }
        },
        "compete_matrix": {
            "name": "compete_matrix",
            "display_name": "竞品分析矩阵",
            "icon": "matrix",
            "category": "business",
            "description": "多维度竞品对比分析矩阵",
            "default_schema": {
                "competitors": [],
                "dimensions": [],
                "components": _create_compete_matrix_components.__func__(),
            }
        },
        "swot": {
            "name": "swot",
            "display_name": "SWOT分析",
            "icon": "chart",
            "category": "business",
            "description": "优势、劣势、机会、威胁四象限分析",
            "default_schema": {
                "strengths": [],
                "weaknesses": [],
                "opportunities": [],
                "threats": [],
                "components": _create_swot_components.__func__(),
            }
        },
        "market_brief": {
            "name": "market_brief",
            "display_name": "市场简报",
            "icon": "briefcase",
            "category": "business",
            "description": "市场调研数据与分析简报",
            "default_schema": {
                "segments": [],
                "components": _create_market_brief_components.__func__(),
            }
        },
        "biz_plan_outline": {
            "name": "biz_plan_outline",
            "display_name": "商业计划书大纲",
            "icon": "document",
            "category": "business",
            "description": "商业计划书章节结构与步骤指引",
            "default_schema": {
                "sections": [],
                "current_step": 0,
                "components": _create_biz_plan_outline_components.__func__(),
            }
        },
        "pricing_strategy": {
            "name": "pricing_strategy",
            "display_name": "定价策略",
            "icon": "tag",
            "category": "business",
            "description": "产品定价策略与价格体系设计",
            "default_schema": {
                "tiers": [],
                "components": _create_pricing_strategy_components.__func__(),
            }
        },
        "channel_strategy": {
            "name": "channel_strategy",
            "display_name": "渠道策略",
            "icon": "share",
            "category": "business",
            "description": "市场推广与销售渠道策略规划",
            "default_schema": {
                "channels": [],
                "components": _create_channel_strategy_components.__func__(),
            }
        },
        "pitch_deck": {
            "name": "pitch_deck",
            "display_name": "路演PPT",
            "icon": "presentation",
            "category": "business",
            "description": "项目路演演示文稿大纲与内容",
            "default_schema": {
                "slides": [],
                "components": _create_pitch_deck_components.__func__(),
            }
        },
        "revenue_model": {
            "name": "revenue_model",
            "display_name": "收入模型",
            "icon": "chart",
            "category": "business",
            "description": "收入来源分析与盈利模式设计",
            "default_schema": {
                "streams": [],
                "components": _create_revenue_model_components.__func__(),
            }
        },
    }
