"""
学术领域页面模板 - 论文大纲、文献矩阵、实验设计、数据分析、田野笔记、伦理审查
"""
from app.page_components import (
    PageTemplate,
    TextBlockComponent, TableComponent, StepsComponent, ListComponent, FileRepoComponent,
    DataChartComponent, DividerComponent, SpacerComponent,
)


class AcademicPages:
    """学术领域页面模板"""

    @staticmethod
    def _create_paper_outline_components() -> list:
        template = PageTemplate(name="paper_outline", display_name="论文大纲", icon="file-text", category="academic", description="学术论文结构规划")
        template.add_component(TextBlockComponent(id="title", content="论文大纲", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="规划学术论文的整体结构和章节安排。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(StepsComponent(
            id="paper_steps",
            steps=[
                {"id": "intro", "title": "引言", "description": "研究背景与问题提出", "status": "pending"},
                {"id": "lit_review", "title": "文献综述", "description": "相关研究回顾", "status": "pending"},
                {"id": "method", "title": "研究方法", "description": "实验设计与数据收集", "status": "pending"},
                {"id": "results", "title": "研究结果", "description": "数据分析与发现", "status": "pending"},
                {"id": "discussion", "title": "讨论", "description": "结果解释与意义", "status": "pending"},
            ],
            current=0,
            order=3,
        ))
        template.add_component(TextBlockComponent(id="notes", content="研究要点记录...", sub_type="paragraph", placeholder="在此记录论文各章节的关键要点和写作思路", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_lit_review_matrix_components() -> list:
        template = PageTemplate(name="lit_review_matrix", display_name="文献矩阵", icon="grid", category="academic", description="文献综述对比矩阵")
        template.add_component(TextBlockComponent(id="title", content="文献综述矩阵", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="系统整理和对比相关文献的核心信息。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TableComponent(
            id="lit_table",
            columns=[
                {"key": "author", "title": "作者/年份", "width": "20%"},
                {"key": "title", "title": "文献标题", "width": "25%"},
                {"key": "method", "title": "研究方法", "width": "15%"},
                {"key": "finding", "title": "主要发现", "width": "25%"},
                {"key": "gap", "title": "研究空白", "width": "15%"},
            ],
            data=[
                {"author": "示例(2024)", "title": "相关研究标题", "method": "实验法", "finding": "主要结论", "gap": "待探索方向"},
            ],
            order=3,
        ))
        template.add_component(TextBlockComponent(id="summary", content="文献综述小结：归纳研究趋势和本文定位。", sub_type="paragraph", placeholder="总结文献综述的核心发现和研究缺口", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_experiment_design_components() -> list:
        template = PageTemplate(name="experiment_design", display_name="实验设计", icon="flask", category="academic", description="科学实验方案设计")
        template.add_component(TextBlockComponent(id="title", content="实验设计", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="详细设计实验步骤、变量控制与数据采集方案。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(StepsComponent(
            id="experiment_steps",
            steps=[
                {"id": "hypothesis", "title": "提出假设", "description": "明确研究假设", "status": "pending"},
                {"id": "setup", "title": "实验设置", "description": "确定变量与条件", "status": "pending"},
                {"id": "procedure", "title": "实验流程", "description": "详细操作步骤", "status": "pending"},
                {"id": "collection", "title": "数据收集", "description": "采集实验数据", "status": "pending"},
            ],
            current=0,
            order=3,
        ))
        template.add_component(TableComponent(
            id="variables",
            columns=[
                {"key": "name", "title": "变量名称", "width": "20%"},
                {"key": "type", "title": "变量类型", "width": "20%"},
                {"key": "description", "title": "描述", "width": "30%"},
                {"key": "measurement", "title": "测量方式", "width": "30%"},
            ],
            data=[
                {"name": "自变量", "type": "独立变量", "description": "操纵的条件", "measurement": "水平设置"},
                {"name": "因变量", "type": "依赖变量", "description": "测量的结果", "measurement": "指标记录"},
            ],
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_data_analysis_plan_components() -> list:
        template = PageTemplate(name="data_analysis_plan", display_name="数据分析计划", icon="chart-bar", category="academic", description="数据分析方案与统计方法")
        template.add_component(TextBlockComponent(id="title", content="数据分析计划", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="规划数据分析流程、统计方法和可视化方案。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(DataChartComponent(
            id="data_chart",
            chart_type="bar",
            labels=["指标A", "指标B", "指标C", "指标D"],
            datasets=[{"label": "实验组", "data": [85, 72, 90, 68]}, {"label": "对照组", "data": [65, 58, 70, 55]}],
            options={"title": "预期结果对比"},
            order=3,
        ))
        template.add_component(TableComponent(
            id="analysis_methods",
            columns=[
                {"key": "question", "title": "研究问题", "width": "25%"},
                {"key": "method", "title": "统计方法", "width": "25%"},
                {"key": "variables", "title": "涉及变量", "width": "25%"},
                {"key": "expected", "title": "预期输出", "width": "25%"},
            ],
            data=[
                {"question": "组间差异", "method": "t检验", "variables": "组别, 得分", "expected": "p值, 效应量"},
            ],
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_field_notes_components() -> list:
        template = PageTemplate(name="field_notes", display_name="田野笔记", icon="book", category="academic", description="实地调研观察记录")
        template.add_component(TextBlockComponent(id="title", content="田野笔记", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="记录实地调研中的观察、访谈和反思。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TextBlockComponent(id="observation", content="观察记录：描述实地观察到的现象和细节。", sub_type="quote", placeholder="详细记录观察到的现象、时间和环境", order=3))
        template.add_component(TextBlockComponent(id="reflection", content="研究反思：记录方法论反思和初步分析。", sub_type="paragraph", placeholder="记录对观察的分析、解释和自我反思", order=4))
        template.add_component(FileRepoComponent(id="field_files", files=[], allow_upload=True, order=5))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_ethics_checklist_components() -> list:
        template = PageTemplate(name="ethics_checklist", display_name="伦理审查清单", icon="check-square", category="academic", description="研究伦理合规审查")
        template.add_component(TextBlockComponent(id="title", content="伦理审查清单", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="确保研究符合学术伦理规范和合规要求。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(ListComponent(
            id="ethics_items",
            items=[
                {"label": "知情同意书已签署", "value": "consent", "description": "参与者已了解研究目的和风险", "checked": False},
                {"label": "数据匿名化处理", "value": "anonymize", "description": "个人身份信息已去除", "checked": False},
                {"label": "隐私保护措施到位", "value": "privacy", "description": "数据存储和传输加密", "checked": False},
                {"label": "伦理委员会审批通过", "value": "approval", "description": "已获得伦理审查批准号", "checked": False},
                {"label": "利益冲突声明提交", "value": "conflict", "description": "已申报潜在利益冲突", "checked": False},
            ],
            show_checkbox=True,
            list_type="simple",
            order=3,
        ))
        template.add_component(TextBlockComponent(id="approval_info", content="审批信息：记录伦理审批编号和日期。", sub_type="paragraph", placeholder="伦理批准编号、批准日期、有效期", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    PAGE_TYPES = {
        "paper_outline": {
            "name": "paper_outline", "display_name": "论文大纲", "icon": "file-text",
            "category": "academic", "description": "学术论文结构规划",
            "default_schema": {"sections": [], "components": _create_paper_outline_components.__func__()}
        },
        "lit_review_matrix": {
            "name": "lit_review_matrix", "display_name": "文献矩阵", "icon": "grid",
            "category": "academic", "description": "文献综述对比矩阵",
            "default_schema": {"references": [], "components": _create_lit_review_matrix_components.__func__()}
        },
        "experiment_design": {
            "name": "experiment_design", "display_name": "实验设计", "icon": "flask",
            "category": "academic", "description": "科学实验方案设计",
            "default_schema": {"hypothesis": "", "variables": [], "components": _create_experiment_design_components.__func__()}
        },
        "data_analysis_plan": {
            "name": "data_analysis_plan", "display_name": "数据分析计划", "icon": "chart-bar",
            "category": "academic", "description": "数据分析方案与统计方法",
            "default_schema": {"methods": [], "components": _create_data_analysis_plan_components.__func__()}
        },
        "field_notes": {
            "name": "field_notes", "display_name": "田野笔记", "icon": "book",
            "category": "academic", "description": "实地调研观察记录",
            "default_schema": {"observations": [], "components": _create_field_notes_components.__func__()}
        },
        "ethics_checklist": {
            "name": "ethics_checklist", "display_name": "伦理审查清单", "icon": "check-square",
            "category": "academic", "description": "研究伦理合规审查",
            "default_schema": {"checklist": [], "components": _create_ethics_checklist_components.__func__()}
        },
    }
