"""
通用功能型组件 - 分隔线、空白占位、多列布局、选项卡、锚点目录
"""
from typing import Any, Optional
from .base import Component, ComponentType


class DividerComponent(Component):
    """分隔线组件"""

    def __init__(
        self,
        style: str = "solid",
        text: str = "",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.DIVIDER,
            id=id, title=title, description=description,
            visible=visible, order=order,
            style=style, text=text,
        )
        self.style = style
        self.text = text

    def get_data(self) -> dict[str, Any]:
        return {"style": self.style, "text": self.text}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "style": {"type": "string", "title": "线条样式", "enum": ["solid", "dashed", "dotted"], "default": "solid"},
                "text": {"type": "string", "title": "文字（可选）", "default": ""},
            },
        }


class SpacerComponent(Component):
    """空白占位组件"""

    def __init__(
        self,
        height: int = 24,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.SPACER,
            id=id, title=title, description=description,
            visible=visible, order=order,
            height=height,
        )
        self.height = height

    def get_data(self) -> dict[str, Any]:
        return {"height": self.height}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "height": {"type": "integer", "title": "高度(px)", "minimum": 4, "maximum": 200, "default": 24},
            },
        }


class MultiColumnComponent(Component):
    """多列布局组件"""

    def __init__(
        self,
        columns: int = 2,
        column_ratios: list[int] = None,
        gap: str = "16px",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.MULTI_COLUMN,
            id=id, title=title, description=description,
            visible=visible, order=order,
            columns=columns, column_ratios=column_ratios or [],
            gap=gap,
        )
        self.columns = columns
        self.column_ratios = column_ratios or []
        self.gap = gap

    def get_data(self) -> dict[str, Any]:
        return {"columns": self.columns, "column_ratios": self.column_ratios, "gap": self.gap}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "columns": {"type": "integer", "title": "列数", "minimum": 2, "maximum": 4, "default": 2},
                "column_ratios": {"type": "array", "title": "列宽比例", "items": {"type": "integer"}, "default": []},
                "gap": {"type": "string", "title": "间距", "default": "16px"},
            },
            "required": ["columns"],
        }


class TabsComponent(Component):
    """选项卡组件"""

    def __init__(
        self,
        tabs: list[dict[str, Any]] = None,
        tab_position: str = "top",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.TABS,
            id=id, title=title, description=description,
            visible=visible, order=order,
            tabs=tabs or [], tab_position=tab_position,
        )
        self.tabs = tabs or []
        self.tab_position = tab_position

    def get_data(self) -> dict[str, Any]:
        return {"tabs": self.tabs, "tab_position": self.tab_position}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "tabs": {"type": "array", "title": "选项卡列表", "items": {"type": "object", "properties": {
                    "key": {"type": "string"}, "label": {"type": "string"},
                    "icon": {"type": "string"}, "content": {"type": "array", "items": {"type": "object"}},
                }}, "default": []},
                "tab_position": {"type": "string", "title": "选项卡位置", "enum": ["top", "side"], "default": "top"},
            },
            "required": ["tabs"],
        }


class AnchorTocComponent(Component):
    """锚点目录组件"""

    def __init__(
        self,
        headings: list[dict[str, Any]] = None,
        sticky: bool = True,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.ANCHOR_TOC,
            id=id, title=title, description=description,
            visible=visible, order=order,
            headings=headings or [], sticky=sticky,
        )
        self.headings = headings or []
        self.sticky = sticky

    def get_data(self) -> dict[str, Any]:
        return {"headings": self.headings, "sticky": self.sticky}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "headings": {"type": "array", "title": "标题列表", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "text": {"type": "string"},
                    "level": {"type": "integer"}, "anchor": {"type": "string"},
                }}, "default": []},
                "sticky": {"type": "boolean", "title": "固定定位", "default": True},
            },
        }
