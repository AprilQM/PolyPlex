"""
数据与度量组件 - 指标卡、进度条、计数器、评分表、测算公式
"""
from typing import Any, Optional
from .base import Component, ComponentType


class MetricCardComponent(Component):
    """指标卡组件"""

    def __init__(
        self,
        value: str = "",
        label: str = "",
        prefix: str = "",
        suffix: str = "",
        trend: Optional[str] = None,
        trend_value: str = "",
        target_value: Optional[str] = None,
        size: str = "medium",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.METRIC_CARD,
            id=id, title=title, description=description,
            visible=visible, order=order,
            value=value, label=label, prefix=prefix, suffix=suffix,
            trend=trend, trend_value=trend_value,
            target_value=target_value, size=size,
        )
        self.value = value
        self.label = label
        self.prefix = prefix
        self.suffix = suffix
        self.trend = trend
        self.trend_value = trend_value
        self.target_value = target_value
        self.size = size

    def get_data(self) -> dict[str, Any]:
        return {"value": self.value, "label": self.label, "prefix": self.prefix,
                "suffix": self.suffix, "trend": self.trend, "trend_value": self.trend_value,
                "target_value": self.target_value, "size": self.size}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "value": {"type": "string", "title": "数值", "default": ""},
                "label": {"type": "string", "title": "标签", "default": ""},
                "prefix": {"type": "string", "title": "前缀", "default": ""},
                "suffix": {"type": "string", "title": "后缀", "default": ""},
                "trend": {"type": ["string", "null"], "title": "趋势", "enum": ["up", "down", None], "default": None},
                "trend_value": {"type": "string", "title": "趋势值", "default": ""},
                "target_value": {"type": ["string", "null"], "title": "目标值", "default": None},
                "size": {"type": "string", "title": "尺寸", "enum": ["small", "medium", "large"], "default": "medium"},
            },
            "required": ["value", "label"],
        }


class ProgressBarComponent(Component):
    """进度条组件"""

    def __init__(
        self,
        percentage: float = 0,
        style: str = "bar",
        color: str = "#1890FF",
        show_label: bool = True,
        target_value: Optional[float] = None,
        current_value: Optional[float] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.PROGRESS_BAR,
            id=id, title=title, description=description,
            visible=visible, order=order,
            percentage=percentage, style=style, color=color,
            show_label=show_label, target_value=target_value, current_value=current_value,
        )
        self.percentage = percentage
        self.style = style
        self.color = color
        self.show_label = show_label
        self.target_value = target_value
        self.current_value = current_value

    def get_data(self) -> dict[str, Any]:
        return {"percentage": self.percentage, "style": self.style, "color": self.color,
                "show_label": self.show_label, "target_value": self.target_value, "current_value": self.current_value}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "percentage": {"type": "number", "title": "百分比", "minimum": 0, "maximum": 100, "default": 0},
                "style": {"type": "string", "title": "样式", "enum": ["bar", "circle", "dashboard"], "default": "bar"},
                "color": {"type": "string", "title": "颜色", "default": "#1890FF"},
                "show_label": {"type": "boolean", "title": "显示标签", "default": True},
                "target_value": {"type": ["number", "null"], "title": "目标值", "default": None},
                "current_value": {"type": ["number", "null"], "title": "当前值", "default": None},
            },
        }


class CounterComponent(Component):
    """计数器组件"""

    def __init__(
        self,
        value: int = 0,
        step: int = 1,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        label: str = "",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.COUNTER,
            id=id, title=title, description=description,
            visible=visible, order=order,
            value=value, step=step, min_value=min_value,
            max_value=max_value, label=label,
        )
        self.value = value
        self.step = step
        self.min_value = min_value
        self.max_value = max_value
        self.label = label

    def get_data(self) -> dict[str, Any]:
        return {"value": self.value, "step": self.step,
                "min_value": self.min_value, "max_value": self.max_value, "label": self.label}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "value": {"type": "integer", "title": "当前值", "default": 0},
                "step": {"type": "integer", "title": "步长", "default": 1},
                "min_value": {"type": ["integer", "null"], "title": "最小值", "default": None},
                "max_value": {"type": ["integer", "null"], "title": "最大值", "default": None},
                "label": {"type": "string", "title": "标签", "default": ""},
            },
        }


class ScorecardComponent(Component):
    """评分表组件"""

    def __init__(
        self,
        dimensions: list[dict[str, Any]] = None,
        score_type: str = "star",
        show_average: bool = True,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.SCORECARD,
            id=id, title=title, description=description,
            visible=visible, order=order,
            dimensions=dimensions or [], score_type=score_type, show_average=show_average,
        )
        self.dimensions = dimensions or []
        self.score_type = score_type
        self.show_average = show_average

    def get_data(self) -> dict[str, Any]:
        return {"dimensions": self.dimensions, "score_type": self.score_type, "show_average": self.show_average}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "dimensions": {"type": "array", "title": "评分维度", "items": {"type": "object", "properties": {
                    "name": {"type": "string"}, "weight": {"type": "number"},
                    "max_score": {"type": "number"}, "score": {"type": "number"},
                }}, "default": []},
                "score_type": {"type": "string", "title": "评分方式", "enum": ["star", "numeric", "slider", "yes_no"], "default": "star"},
                "show_average": {"type": "boolean", "title": "显示平均分", "default": True},
            },
        }


class FormulaComponent(Component):
    """测算公式组件"""

    def __init__(
        self,
        formula: str = "",
        variables: list[dict[str, Any]] = None,
        result: Optional[str] = None,
        formula_type: str = "custom",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.FORMULA,
            id=id, title=title, description=description,
            visible=visible, order=order,
            formula=formula, variables=variables or [],
            result=result, formula_type=formula_type,
        )
        self.formula = formula
        self.variables = variables or []
        self.result = result
        self.formula_type = formula_type

    def get_data(self) -> dict[str, Any]:
        return {"formula": self.formula, "variables": self.variables,
                "result": self.result, "formula_type": self.formula_type}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "formula": {"type": "string", "title": "公式表达式", "default": ""},
                "variables": {"type": "array", "title": "变量定义", "items": {"type": "object", "properties": {
                    "name": {"type": "string"}, "label": {"type": "string"},
                    "value": {"type": "number"}, "type": {"type": "string"},
                }}, "default": []},
                "result": {"type": ["string", "null"], "title": "计算结果", "default": None},
                "formula_type": {"type": "string", "title": "公式类型",
                                 "enum": ["custom", "ltv", "cac", "roi", "nps"], "default": "custom"},
            },
        }
