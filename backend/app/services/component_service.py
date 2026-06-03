"""
组件类型元数据服务 - 提供默认数据、Schema、分类映射
"""
from app.page_components.base import ComponentType

# 八大分类
CATEGORY_NAMES = {
    "basic": "基础内容",
    "structured": "结构化",
    "visualization": "可视化",
    "metric": "数据与度量",
    "collaboration": "协作",
    "reference": "引用与关联",
    "domain_specific": "领域专用",
    "utility": "通用功能",
}

COMPONENT_TYPE_CATEGORY: dict[ComponentType, str] = {
    # 基础内容
    ComponentType.TEXT_BLOCK: "basic",
    ComponentType.IMAGE_GALLERY: "basic",
    ComponentType.VIDEO_EMBED: "basic",
    ComponentType.AUDIO_PLAYER: "basic",
    ComponentType.FILE_REPO: "basic",
    ComponentType.ATTACHMENT_LIST: "basic",
    # 结构化
    ComponentType.TABLE: "structured",
    ComponentType.KANBAN: "structured",
    ComponentType.TIMELINE: "structured",
    ComponentType.STEPS: "structured",
    ComponentType.LIST: "structured",
    # 可视化
    ComponentType.MINDMAP: "visualization",
    ComponentType.FLOWCHART: "visualization",
    ComponentType.RELATION_GRAPH: "visualization",
    ComponentType.DATA_CHART: "visualization",
    ComponentType.MOODBOARD: "visualization",
    ComponentType.WHITEBOARD: "visualization",
    # 数据与度量
    ComponentType.METRIC_CARD: "metric",
    ComponentType.PROGRESS_BAR: "metric",
    ComponentType.COUNTER: "metric",
    ComponentType.SCORECARD: "metric",
    ComponentType.FORMULA: "metric",
    # 协作
    ComponentType.COMMENT_ANCHOR: "collaboration",
    ComponentType.VOTE_MODULE: "collaboration",
    ComponentType.TASK_ASSIGN: "collaboration",
    ComponentType.CHANGELOG: "collaboration",
    # 引用与关联
    ComponentType.PAGE_REF: "reference",
    ComponentType.EMBED_VIEW: "reference",
    ComponentType.BREADCRUMB: "reference",
    ComponentType.TAG_SET: "reference",
    # 领域专用
    ComponentType.BIZ_CANVAS: "domain_specific",
    ComponentType.PERSONA_CARD: "domain_specific",
    ComponentType.SWOT: "domain_specific",
    ComponentType.COMPETE_MATRIX: "domain_specific",
    ComponentType.STORY_TREE: "domain_specific",
    ComponentType.CHARACTER_CARD: "domain_specific",
    ComponentType.CHAPTER_TABLE: "domain_specific",
    ComponentType.STORYBOARD: "domain_specific",
    ComponentType.LEVEL_DESIGN: "domain_specific",
    ComponentType.COURSE_OUTLINE: "domain_specific",
    ComponentType.CONTENT_CALENDAR: "domain_specific",
    ComponentType.FUNNEL: "domain_specific",
    ComponentType.EXPERIMENT: "domain_specific",
    # 通用功能
    ComponentType.DIVIDER: "utility",
    ComponentType.SPACER: "utility",
    ComponentType.MULTI_COLUMN: "utility",
    ComponentType.TABS: "utility",
    ComponentType.ANCHOR_TOC: "utility",
    # 代码仓库
    ComponentType.GIT_REPO: "basic",
}


def get_category_name(category_key: str) -> str:
    """获取分类的中文名称"""
    return CATEGORY_NAMES.get(category_key, category_key)


def get_components_by_category(category: str) -> list[dict]:
    """获取某分类下的所有组件类型信息"""
    result = []
    for ct, cat in COMPONENT_TYPE_CATEGORY.items():
        if cat == category:
            result.append({
                "type": ct.value,
                "name": ct.name,
                "category": category,
                "category_name": get_category_name(category),
            })
    return result


def get_all_component_types() -> list[dict]:
    """获取所有组件类型的元数据"""
    result = []
    for ct in ComponentType:
        cat = COMPONENT_TYPE_CATEGORY.get(ct, "uncategorized")
        result.append({
            "type": ct.value,
            "name": ct.name,
            "category": cat,
            "category_name": get_category_name(cat),
        })
    return result


def get_component_category_map() -> dict[str, list[dict]]:
    """获取按分类分组的组件类型映射"""
    result = {}
    for ct, cat in COMPONENT_TYPE_CATEGORY.items():
        if cat not in result:
            result[cat] = []
        result[cat].append({
            "type": ct.value,
            "name": ct.name,
        })
    return result
