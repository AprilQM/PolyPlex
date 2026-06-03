"""
页面模板初始化文件 - 全部 11 个领域，93 个页面模板
"""
from app.project_templates.general import GeneralPages
from app.project_templates.code import CodePages
from app.project_templates.writing import WritingPages
from app.project_templates.design import DesignPages
from app.project_templates.business import BusinessPages
from app.project_templates.lifestyle import LifestylePages
from app.project_templates.other import OtherPages
from app.project_templates.academic import AcademicPages
from app.project_templates.media import MediaPages
from app.project_templates.education import EducationPages
from app.project_templates.marketing import MarketingPages
from app.project_templates.music import MusicPages

# 合并所有页面类型
ALL_PAGE_TYPES = {
    **GeneralPages.PAGE_TYPES,
    **CodePages.PAGE_TYPES,
    **WritingPages.PAGE_TYPES,
    **DesignPages.PAGE_TYPES,
    **BusinessPages.PAGE_TYPES,
    **LifestylePages.PAGE_TYPES,
    **OtherPages.PAGE_TYPES,
    **AcademicPages.PAGE_TYPES,
    **MediaPages.PAGE_TYPES,
    **EducationPages.PAGE_TYPES,
    **MarketingPages.PAGE_TYPES,
    **MusicPages.PAGE_TYPES,
}

# 按分类获取
PAGE_TYPES_BY_CATEGORY = {
    "general": GeneralPages.PAGE_TYPES,
    "code": CodePages.PAGE_TYPES,
    "writing": WritingPages.PAGE_TYPES,
    "design": DesignPages.PAGE_TYPES,
    "business": BusinessPages.PAGE_TYPES,
    "lifestyle": LifestylePages.PAGE_TYPES,
    "other": OtherPages.PAGE_TYPES,
    "academic": AcademicPages.PAGE_TYPES,
    "media": MediaPages.PAGE_TYPES,
    "education": EducationPages.PAGE_TYPES,
    "marketing": MarketingPages.PAGE_TYPES,
    "music": MusicPages.PAGE_TYPES,
}


def get_page_type_info(page_type: str) -> dict | None:
    """获取单个页面类型的详细信息"""
    return ALL_PAGE_TYPES.get(page_type)


def get_page_types_by_category(category: str = None) -> dict:
    """按分类获取页面类型"""
    if category:
        return PAGE_TYPES_BY_CATEGORY.get(category, {})
    return ALL_PAGE_TYPES


def get_page_type_choices() -> list:
    """获取用于表单选择的页面类型列表"""
    return [(key, info["display_name"]) for key, info in ALL_PAGE_TYPES.items()]


__all__ = [
    "GeneralPages", "CodePages", "WritingPages", "DesignPages",
    "BusinessPages", "LifestylePages", "OtherPages",
    "AcademicPages", "MediaPages", "EducationPages",
    "MarketingPages", "MusicPages",
    "ALL_PAGE_TYPES", "PAGE_TYPES_BY_CATEGORY",
    "get_page_type_info", "get_page_types_by_category", "get_page_type_choices",
]
