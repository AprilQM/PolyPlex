"""
结构化组件 - 表格、看板、时间线、步骤条、列表
"""
from typing import Any, Optional
from .base import Component, ComponentType


class TableComponent(Component):
    """表格组件"""

    def __init__(
        self,
        columns: list[dict[str, Any]] = None,
        data: list[dict[str, Any]] = None,
        show_border: bool = True,
        striped: bool = False,
        hoverable: bool = True,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.TABLE,
            id=id, title=title, description=description,
            visible=visible, order=order,
            columns=columns or [], data=data or [],
            show_border=show_border, striped=striped, hoverable=hoverable,
        )
        self.columns = columns or []
        self.data = data or []
        self.show_border = show_border
        self.striped = striped
        self.hoverable = hoverable

    def get_data(self) -> dict[str, Any]:
        return {"columns": self.columns, "data": self.data,
                "show_border": self.show_border, "striped": self.striped, "hoverable": self.hoverable}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "columns": {"type": "array", "title": "列定义", "items": {"type": "object"}, "default": []},
                "data": {"type": "array", "title": "表格数据", "items": {"type": "object"}, "default": []},
                "show_border": {"type": "boolean", "title": "显示边框", "default": True},
                "striped": {"type": "boolean", "title": "斑马纹", "default": False},
                "hoverable": {"type": "boolean", "title": "悬停高亮", "default": True},
            },
            "required": ["columns", "data"],
        }


class KanbanComponent(Component):
    """看板组件"""

    def __init__(
        self,
        columns: list[dict[str, Any]] = None,
        cards: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.KANBAN,
            id=id, title=title, description=description,
            visible=visible, order=order,
            columns=columns or [], cards=cards or [],
        )
        self.columns = columns or []
        self.cards = cards or []

    def get_data(self) -> dict[str, Any]:
        return {"columns": self.columns, "cards": self.cards}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "columns": {"type": "array", "title": "看板列", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "title": {"type": "string"}, "color": {"type": "string"},
                }}, "default": []},
                "cards": {"type": "array", "title": "卡片列表", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "title": {"type": "string"}, "description": {"type": "string"},
                    "column_id": {"type": "string"}, "priority": {"type": "string"},
                    "assignee": {"type": "string"}, "due_date": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                }}, "default": []},
            },
            "required": ["columns"],
        }


class TimelineComponent(Component):
    """时间线组件"""

    def __init__(
        self,
        events: list[dict[str, Any]] = None,
        layout: str = "vertical",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.TIMELINE,
            id=id, title=title, description=description,
            visible=visible, order=order,
            events=events or [], layout=layout,
        )
        self.events = events or []
        self.layout = layout

    def get_data(self) -> dict[str, Any]:
        return {"events": self.events, "layout": self.layout}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "events": {"type": "array", "title": "事件列表", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "title": {"type": "string"}, "description": {"type": "string"},
                    "date": {"type": "string"}, "time": {"type": "string"},
                    "icon": {"type": "string"}, "color": {"type": "string"},
                    "start_date": {"type": "string"}, "end_date": {"type": "string"},
                }}, "default": []},
                "layout": {"type": "string", "title": "布局", "enum": ["vertical", "horizontal"], "default": "vertical"},
            },
            "required": ["events"],
        }


class StepsComponent(Component):
    """步骤条组件"""

    def __init__(
        self,
        steps: list[dict[str, Any]] = None,
        layout: str = "horizontal",
        current: int = 0,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.STEPS,
            id=id, title=title, description=description,
            visible=visible, order=order,
            steps=steps or [], layout=layout, current=current,
        )
        self.steps = steps or []
        self.layout = layout
        self.current = current

    def get_data(self) -> dict[str, Any]:
        return {"steps": self.steps, "layout": self.layout, "current": self.current}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "steps": {"type": "array", "title": "步骤列表", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "title": {"type": "string"}, "description": {"type": "string"},
                    "status": {"type": "string", "enum": ["pending", "in_progress", "completed", "error"]},
                }}, "default": []},
                "layout": {"type": "string", "title": "布局", "enum": ["horizontal", "vertical"], "default": "horizontal"},
                "current": {"type": "integer", "title": "当前步骤", "default": 0},
            },
            "required": ["steps"],
        }


class ListComponent(Component):
    """列表组件 - 支持简单清单、排序列表、定义列表、属性列表"""

    def __init__(
        self,
        items: list[dict[str, Any]] = None,
        list_type: str = "simple",
        show_checkbox: bool = False,
        show_index: bool = False,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.LIST,
            id=id, title=title, description=description,
            visible=visible, order=order,
            items=items or [], list_type=list_type,
            show_checkbox=show_checkbox, show_index=show_index,
        )
        self.items = items or []
        self.list_type = list_type
        self.show_checkbox = show_checkbox
        self.show_index = show_index

    def get_data(self) -> dict[str, Any]:
        return {"items": self.items, "list_type": self.list_type,
                "show_checkbox": self.show_checkbox, "show_index": self.show_index}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "items": {"type": "array", "title": "列表项", "items": {"type": "object", "properties": {
                    "label": {"type": "string"}, "value": {"type": "string"},
                    "description": {"type": "string"}, "icon": {"type": "string"},
                    "checked": {"type": "boolean"},
                }}, "default": []},
                "list_type": {"type": "string", "title": "列表类型",
                              "enum": ["simple", "sorted", "definition", "property"], "default": "simple"},
                "show_checkbox": {"type": "boolean", "title": "显示复选框", "default": False},
                "show_index": {"type": "boolean", "title": "显示序号", "default": False},
            },
            "required": ["items"],
        }
