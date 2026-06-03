"""
引用与关联组件 - 页面引用、嵌入视图、面包屑导航、标签集
"""
from typing import Any, Optional
from .base import Component, ComponentType


class PageRefComponent(Component):
    """页面引用组件"""

    def __init__(
        self,
        ref_type: str = "link",
        ref_page_id: Optional[int] = None,
        ref_project_id: Optional[int] = None,
        ref_url: str = "",
        display_title: str = "",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.PAGE_REF,
            id=id, title=title, description=description,
            visible=visible, order=order,
            ref_type=ref_type, ref_page_id=ref_page_id,
            ref_project_id=ref_project_id, ref_url=ref_url, display_title=display_title,
        )
        self.ref_type = ref_type
        self.ref_page_id = ref_page_id
        self.ref_project_id = ref_project_id
        self.ref_url = ref_url
        self.display_title = display_title

    def get_data(self) -> dict[str, Any]:
        return {"ref_type": self.ref_type, "ref_page_id": self.ref_page_id,
                "ref_project_id": self.ref_project_id, "ref_url": self.ref_url,
                "display_title": self.display_title}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "ref_type": {"type": "string", "title": "引用方式", "enum": ["link", "card", "inline"], "default": "link"},
                "ref_page_id": {"type": ["integer", "null"], "title": "引用页面ID", "default": None},
                "ref_project_id": {"type": ["integer", "null"], "title": "引用项目ID", "default": None},
                "ref_url": {"type": "string", "title": "外部URL", "default": ""},
                "display_title": {"type": "string", "title": "显示标题", "default": ""},
            },
        }


class EmbedViewComponent(Component):
    """嵌入视图组件"""

    def __init__(
        self,
        url: str = "",
        embed_type: str = "iframe",
        width: str = "100%",
        height: str = "400px",
        allow_fullscreen: bool = True,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.EMBED_VIEW,
            id=id, title=title, description=description,
            visible=visible, order=order,
            url=url, embed_type=embed_type, width=width,
            height=height, allow_fullscreen=allow_fullscreen,
        )
        self.url = url
        self.embed_type = embed_type
        self.width = width
        self.height = height
        self.allow_fullscreen = allow_fullscreen

    def get_data(self) -> dict[str, Any]:
        return {"url": self.url, "embed_type": self.embed_type, "width": self.width,
                "height": self.height, "allow_fullscreen": self.allow_fullscreen}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "title": "嵌入URL", "default": ""},
                "embed_type": {"type": "string", "title": "嵌入类型", "default": "iframe"},
                "width": {"type": "string", "title": "宽度", "default": "100%"},
                "height": {"type": "string", "title": "高度", "default": "400px"},
                "allow_fullscreen": {"type": "boolean", "title": "允许全屏", "default": True},
            },
            "required": ["url"],
        }


class BreadcrumbComponent(Component):
    """面包屑导航组件"""

    def __init__(
        self,
        items: list[dict[str, Any]] = None,
        separator: str = "/",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.BREADCRUMB,
            id=id, title=title, description=description,
            visible=visible, order=order,
            items=items or [], separator=separator,
        )
        self.items = items or []
        self.separator = separator

    def get_data(self) -> dict[str, Any]:
        return {"items": self.items, "separator": self.separator}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "items": {"type": "array", "title": "导航项", "items": {"type": "object", "properties": {
                    "label": {"type": "string"}, "url": {"type": "string"}, "icon": {"type": "string"},
                }}, "default": []},
                "separator": {"type": "string", "title": "分隔符", "default": "/"},
            },
            "required": ["items"],
        }


class TagSetComponent(Component):
    """标签集组件"""

    def __init__(
        self,
        tags: list[dict[str, Any]] = None,
        allow_create: bool = True,
        show_count: bool = False,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.TAG_SET,
            id=id, title=title, description=description,
            visible=visible, order=order,
            tags=tags or [], allow_create=allow_create, show_count=show_count,
        )
        self.tags = tags or []
        self.allow_create = allow_create
        self.show_count = show_count

    def get_data(self) -> dict[str, Any]:
        return {"tags": self.tags, "allow_create": self.allow_create, "show_count": self.show_count}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "tags": {"type": "array", "title": "标签列表", "items": {"type": "object", "properties": {
                    "name": {"type": "string"}, "color": {"type": "string"},
                    "text_color": {"type": "string"}, "count": {"type": "integer"},
                }}, "default": []},
                "allow_create": {"type": "boolean", "title": "允许创建", "default": True},
                "show_count": {"type": "boolean", "title": "显示数量", "default": False},
            },
        }
