"""
可视化组件 - 思维导图、流程图、关系图、数据图表、情绪板、白板
"""
from typing import Any, Optional
from .base import Component, ComponentType


class MindmapComponent(Component):
    """思维导图组件"""

    def __init__(
        self,
        nodes: list[dict[str, Any]] = None,
        layout: str = "tree",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.MINDMAP,
            id=id, title=title, description=description,
            visible=visible, order=order,
            nodes=nodes or [], layout=layout,
        )
        self.nodes = nodes or []
        self.layout = layout

    def get_data(self) -> dict[str, Any]:
        return {"nodes": self.nodes, "layout": self.layout}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "nodes": {"type": "array", "title": "节点列表", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "label": {"type": "string"},
                    "parent_id": {"type": ["string", "null"]}, "color": {"type": "string"},
                    "icon": {"type": "string"}, "collapsed": {"type": "boolean"},
                }}, "default": []},
                "layout": {"type": "string", "title": "布局", "enum": ["tree", "radial", "org"], "default": "tree"},
            },
            "required": ["nodes"],
        }


class FlowchartComponent(Component):
    """流程图组件"""

    def __init__(
        self,
        nodes: list[dict[str, Any]] = None,
        edges: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.FLOWCHART,
            id=id, title=title, description=description,
            visible=visible, order=order,
            nodes=nodes or [], edges=edges or [],
        )
        self.nodes = nodes or []
        self.edges = edges or []

    def get_data(self) -> dict[str, Any]:
        return {"nodes": self.nodes, "edges": self.edges}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "nodes": {"type": "array", "title": "节点列表", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "label": {"type": "string"},
                    "type": {"type": "string", "enum": ["process", "decision", "start_end", "input_output", "subprocess"]},
                    "x": {"type": "number"}, "y": {"type": "number"},
                }}, "default": []},
                "edges": {"type": "array", "title": "连接线", "items": {"type": "object", "properties": {
                    "from": {"type": "string"}, "to": {"type": "string"},
                    "label": {"type": "string"}, "style": {"type": "string", "enum": ["solid", "dashed", "dotted"]},
                }}, "default": []},
            },
            "required": ["nodes"],
        }


class RelationGraphComponent(Component):
    """关系图组件"""

    def __init__(
        self,
        nodes: list[dict[str, Any]] = None,
        edges: list[dict[str, Any]] = None,
        layout: str = "force",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.RELATION_GRAPH,
            id=id, title=title, description=description,
            visible=visible, order=order,
            nodes=nodes or [], edges=edges or [], layout=layout,
        )
        self.nodes = nodes or []
        self.edges = edges or []
        self.layout = layout

    def get_data(self) -> dict[str, Any]:
        return {"nodes": self.nodes, "edges": self.edges, "layout": self.layout}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "nodes": {"type": "array", "title": "节点", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "label": {"type": "string"}, "group": {"type": "string"},
                    "size": {"type": "number"}, "color": {"type": "string"}, "icon": {"type": "string"},
                }}, "default": []},
                "edges": {"type": "array", "title": "边", "items": {"type": "object", "properties": {
                    "from": {"type": "string"}, "to": {"type": "string"},
                    "label": {"type": "string"}, "style": {"type": "string"},
                    "direction": {"type": "string", "enum": ["one_way", "two_way"]},
                }}, "default": []},
                "layout": {"type": "string", "title": "布局算法", "enum": ["force", "hierarchical", "circular"], "default": "force"},
            },
        }


class DataChartComponent(Component):
    """数据图表组件"""

    def __init__(
        self,
        chart_type: str = "bar",
        labels: list[str] = None,
        datasets: list[dict[str, Any]] = None,
        options: dict[str, Any] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.DATA_CHART,
            id=id, title=title, description=description,
            visible=visible, order=order,
            chart_type=chart_type, labels=labels or [],
            datasets=datasets or [], options=options or {},
        )
        self.chart_type = chart_type
        self.labels = labels or []
        self.datasets = datasets or []
        self.options = options or {}

    def get_data(self) -> dict[str, Any]:
        return {"chart_type": self.chart_type, "labels": self.labels,
                "datasets": self.datasets, "options": self.options}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "chart_type": {"type": "string", "title": "图表类型",
                               "enum": ["bar", "line", "pie", "scatter", "radar", "gauge"], "default": "bar"},
                "labels": {"type": "array", "title": "标签", "items": {"type": "string"}, "default": []},
                "datasets": {"type": "array", "title": "数据集", "items": {"type": "object"}, "default": []},
                "options": {"type": "object", "title": "配置选项", "default": {}},
            },
            "required": ["chart_type", "datasets"],
        }


class MoodboardComponent(Component):
    """情绪板组件"""

    def __init__(
        self,
        items: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.MOODBOARD,
            id=id, title=title, description=description,
            visible=visible, order=order,
            items=items or [],
        )
        self.items = items or []

    def get_data(self) -> dict[str, Any]:
        return {"items": self.items}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "items": {"type": "array", "title": "情绪板项目", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "type": {"type": "string", "enum": ["image", "color", "text", "note"]},
                    "content": {"type": "string"}, "x": {"type": "number"}, "y": {"type": "number"},
                    "width": {"type": "number"}, "height": {"type": "number"}, "color": {"type": "string"},
                }}, "default": []},
            },
        }


class WhiteboardComponent(Component):
    """白板组件"""

    def __init__(
        self,
        elements: list[dict[str, Any]] = None,
        background: str = "grid",
        width: int = 1920,
        height: int = 1080,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.WHITEBOARD,
            id=id, title=title, description=description,
            visible=visible, order=order,
            elements=elements or [], background=background,
            width=width, height=height,
        )
        self.elements = elements or []
        self.background = background
        self.width = width
        self.height = height

    def get_data(self) -> dict[str, Any]:
        return {"elements": self.elements, "background": self.background,
                "width": self.width, "height": self.height}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "elements": {"type": "array", "title": "画布元素", "items": {"type": "object"}, "default": []},
                "background": {"type": "string", "title": "背景样式", "enum": ["grid", "dots", "blank"], "default": "grid"},
                "width": {"type": "integer", "title": "宽度", "default": 1920},
                "height": {"type": "integer", "title": "高度", "default": 1080},
            },
        }
