"""
领域专用组件 - 商业画布、用户画像卡、SWOT矩阵、竞品分析矩阵、故事大纲树、角色设定卡、章节细纲表、分镜脚本板、关卡设计文档、课程大纲、内容日历、转化漏斗、实验记录
"""
from typing import Any, Optional
from .base import Component, ComponentType


class BizCanvasComponent(Component):
    """商业画布组件（九宫格）"""

    def __init__(
        self,
        template: str = "lean_canvas",
        cells: dict[str, Any] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.BIZ_CANVAS,
            id=id, title=title, description=description,
            visible=visible, order=order,
            template=template, cells=cells or {},
        )
        self.template = template
        self.cells = cells or {}

    def get_data(self) -> dict[str, Any]:
        return {"template": self.template, "cells": self.cells}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "template": {"type": "string", "title": "画布模板",
                             "enum": ["lean_canvas", "business_model", "blue_ocean"], "default": "lean_canvas"},
                "cells": {"type": "object", "title": "九宫格内容", "default": {}},
            },
            "required": ["template"],
        }


class PersonaCardComponent(Component):
    """用户画像卡组件"""

    def __init__(
        self,
        name: str = "",
        avatar_url: str = "",
        demographics: dict[str, str] = None,
        goals: list[str] = None,
        pain_points: list[str] = None,
        behaviors: list[str] = None,
        scenarios: list[str] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.PERSONA_CARD,
            id=id, title=title, description=description,
            visible=visible, order=order,
            name=name, avatar_url=avatar_url,
            demographics=demographics or {}, goals=goals or [],
            pain_points=pain_points or [], behaviors=behaviors or [],
            scenarios=scenarios or [],
        )
        self.name = name
        self.avatar_url = avatar_url
        self.demographics = demographics or {}
        self.goals = goals or []
        self.pain_points = pain_points or []
        self.behaviors = behaviors or []
        self.scenarios = scenarios or []

    def get_data(self) -> dict[str, Any]:
        return {"name": self.name, "avatar_url": self.avatar_url, "demographics": self.demographics,
                "goals": self.goals, "pain_points": self.pain_points,
                "behaviors": self.behaviors, "scenarios": self.scenarios}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "title": "姓名", "default": ""},
                "avatar_url": {"type": "string", "title": "头像", "default": ""},
                "demographics": {"type": "object", "title": "人口学信息", "default": {}},
                "goals": {"type": "array", "title": "目标", "items": {"type": "string"}, "default": []},
                "pain_points": {"type": "array", "title": "痛点", "items": {"type": "string"}, "default": []},
                "behaviors": {"type": "array", "title": "行为特征", "items": {"type": "string"}, "default": []},
                "scenarios": {"type": "array", "title": "使用场景", "items": {"type": "string"}, "default": []},
            },
            "required": ["name"],
        }


class SwotComponent(Component):
    """SWOT矩阵组件"""

    def __init__(
        self,
        strengths: list[str] = None,
        weaknesses: list[str] = None,
        opportunities: list[str] = None,
        threats: list[str] = None,
        strategies: dict[str, list[str]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.SWOT,
            id=id, title=title, description=description,
            visible=visible, order=order,
            strengths=strengths or [], weaknesses=weaknesses or [],
            opportunities=opportunities or [], threats=threats or [],
            strategies=strategies or {},
        )
        self.strengths = strengths or []
        self.weaknesses = weaknesses or []
        self.opportunities = opportunities or []
        self.threats = threats or []
        self.strategies = strategies or {}

    def get_data(self) -> dict[str, Any]:
        return {"strengths": self.strengths, "weaknesses": self.weaknesses,
                "opportunities": self.opportunities, "threats": self.threats,
                "strategies": self.strategies}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "strengths": {"type": "array", "title": "优势(S)", "items": {"type": "string"}, "default": []},
                "weaknesses": {"type": "array", "title": "劣势(W)", "items": {"type": "string"}, "default": []},
                "opportunities": {"type": "array", "title": "机会(O)", "items": {"type": "string"}, "default": []},
                "threats": {"type": "array", "title": "威胁(T)", "items": {"type": "string"}, "default": []},
                "strategies": {"type": "object", "title": "交叉策略", "default": {}},
            },
        }


class CompeteMatrixComponent(Component):
    """竞品分析矩阵组件"""

    def __init__(
        self,
        competitors: list[str] = None,
        dimensions: list[str] = None,
        scores: dict[str, dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.COMPETE_MATRIX,
            id=id, title=title, description=description,
            visible=visible, order=order,
            competitors=competitors or [], dimensions=dimensions or [],
            scores=scores or {},
        )
        self.competitors = competitors or []
        self.dimensions = dimensions or []
        self.scores = scores or {}

    def get_data(self) -> dict[str, Any]:
        return {"competitors": self.competitors, "dimensions": self.dimensions, "scores": self.scores}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "competitors": {"type": "array", "title": "竞品列表", "items": {"type": "string"}, "default": []},
                "dimensions": {"type": "array", "title": "对比维度", "items": {"type": "string"}, "default": []},
                "scores": {"type": "object", "title": "评分数据", "default": {}},
            },
        }


class StoryTreeComponent(Component):
    """故事大纲树组件"""

    def __init__(
        self,
        nodes: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.STORY_TREE,
            id=id, title=title, description=description,
            visible=visible, order=order,
            nodes=nodes or [],
        )
        self.nodes = nodes or []

    def get_data(self) -> dict[str, Any]:
        return {"nodes": self.nodes}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "nodes": {"type": "array", "title": "大纲节点", "items": {"type": "object", "properties": {
                    "id": {"type": "string"}, "title": {"type": "string"},
                    "parent_id": {"type": ["string", "null"]}, "level": {"type": "integer"},
                    "summary": {"type": "string"}, "word_count": {"type": "integer"},
                    "status": {"type": "string"},
                }}, "default": []},
            },
        }


class CharacterCardComponent(Component):
    """角色设定卡组件"""

    def __init__(
        self,
        name: str = "",
        age: str = "",
        appearance: str = "",
        personality: str = "",
        background: str = "",
        traits: list[str] = None,
        relationships: list[dict[str, str]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.CHARACTER_CARD,
            id=id, title=title, description=description,
            visible=visible, order=order,
            name=name, age=age, appearance=appearance,
            personality=personality, background=background,
            traits=traits or [], relationships=relationships or [],
        )
        self.name = name
        self.age = age
        self.appearance = appearance
        self.personality = personality
        self.background = background
        self.traits = traits or []
        self.relationships = relationships or []

    def get_data(self) -> dict[str, Any]:
        return {"name": self.name, "age": self.age, "appearance": self.appearance,
                "personality": self.personality, "background": self.background,
                "traits": self.traits, "relationships": self.relationships}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "title": "姓名", "default": ""},
                "age": {"type": "string", "title": "年龄", "default": ""},
                "appearance": {"type": "string", "title": "外貌", "default": ""},
                "personality": {"type": "string", "title": "性格", "default": ""},
                "background": {"type": "string", "title": "背景故事", "default": ""},
                "traits": {"type": "array", "title": "特征标签", "items": {"type": "string"}, "default": []},
                "relationships": {"type": "array", "title": "关系网络", "items": {"type": "object", "properties": {
                    "character": {"type": "string"}, "relation": {"type": "string"},
                }}, "default": []},
            },
            "required": ["name"],
        }


class ChapterTableComponent(Component):
    """章节细纲表组件"""

    def __init__(
        self,
        chapters: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.CHAPTER_TABLE,
            id=id, title=title, description=description,
            visible=visible, order=order,
            chapters=chapters or [],
        )
        self.chapters = chapters or []

    def get_data(self) -> dict[str, Any]:
        return {"chapters": self.chapters}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "chapters": {"type": "array", "title": "章节列表", "items": {"type": "object", "properties": {
                    "chapter": {"type": "string"}, "scene": {"type": "string"},
                    "perspective": {"type": "string"}, "event": {"type": "string"},
                    "cliffhanger": {"type": "string"}, "word_count": {"type": "integer"},
                }}, "default": []},
            },
        }


class StoryboardComponent(Component):
    """分镜脚本板组件"""

    def __init__(
        self,
        shots: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.STORYBOARD,
            id=id, title=title, description=description,
            visible=visible, order=order,
            shots=shots or [],
        )
        self.shots = shots or []

    def get_data(self) -> dict[str, Any]:
        return {"shots": self.shots}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "shots": {"type": "array", "title": "镜头列表", "items": {"type": "object", "properties": {
                    "shot_no": {"type": "integer"}, "scene": {"type": "string"},
                    "shot_type": {"type": "string"}, "description": {"type": "string"},
                    "dialogue": {"type": "string"}, "duration": {"type": "number"},
                    "sound": {"type": "string"}, "sketch_url": {"type": "string"},
                }}, "default": []},
            },
        }


class LevelDesignComponent(Component):
    """关卡设计文档组件"""

    def __init__(
        self,
        level_name: str = "",
        theme: str = "",
        difficulty: str = "medium",
        core_mechanic: str = "",
        enemies: list[dict[str, Any]] = None,
        items: list[dict[str, Any]] = None,
        clear_condition: str = "",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.LEVEL_DESIGN,
            id=id, title=title, description=description,
            visible=visible, order=order,
            level_name=level_name, theme=theme, difficulty=difficulty,
            core_mechanic=core_mechanic, enemies=enemies or [],
            items=items or [], clear_condition=clear_condition,
        )
        self.level_name = level_name
        self.theme = theme
        self.difficulty = difficulty
        self.core_mechanic = core_mechanic
        self.enemies = enemies or []
        self.items = items or []
        self.clear_condition = clear_condition

    def get_data(self) -> dict[str, Any]:
        return {"level_name": self.level_name, "theme": self.theme, "difficulty": self.difficulty,
                "core_mechanic": self.core_mechanic, "enemies": self.enemies,
                "items": self.items, "clear_condition": self.clear_condition}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "level_name": {"type": "string", "title": "关卡名称", "default": ""},
                "theme": {"type": "string", "title": "主题", "default": ""},
                "difficulty": {"type": "string", "title": "难度", "enum": ["easy", "medium", "hard"], "default": "medium"},
                "core_mechanic": {"type": "string", "title": "核心机制", "default": ""},
                "enemies": {"type": "array", "title": "敌人配置", "items": {"type": "object"}, "default": []},
                "items": {"type": "array", "title": "道具分布", "items": {"type": "object"}, "default": []},
                "clear_condition": {"type": "string", "title": "通关条件", "default": ""},
            },
            "required": ["level_name"],
        }


class CourseOutlineComponent(Component):
    """课程大纲组件"""

    def __init__(
        self,
        modules: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.COURSE_OUTLINE,
            id=id, title=title, description=description,
            visible=visible, order=order,
            modules=modules or [],
        )
        self.modules = modules or []

    def get_data(self) -> dict[str, Any]:
        return {"modules": self.modules}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "modules": {"type": "array", "title": "课程模块", "items": {"type": "object", "properties": {
                    "module_name": {"type": "string"}, "units": {"type": "array", "items": {"type": "object", "properties": {
                        "title": {"type": "string"}, "objective": {"type": "string"},
                        "activities": {"type": "string"}, "duration": {"type": "string"},
                        "materials": {"type": "array", "items": {"type": "string"}},
                    }}},
                }}, "default": []},
            },
        }


class ContentCalendarComponent(Component):
    """内容日历组件"""

    def __init__(
        self,
        items: list[dict[str, Any]] = None,
        view: str = "calendar",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.CONTENT_CALENDAR,
            id=id, title=title, description=description,
            visible=visible, order=order,
            items=items or [], view=view,
        )
        self.items = items or []
        self.view = view

    def get_data(self) -> dict[str, Any]:
        return {"items": self.items, "view": self.view}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "items": {"type": "array", "title": "内容条目", "items": {"type": "object", "properties": {
                    "title": {"type": "string"}, "type": {"type": "string"},
                    "channel": {"type": "string"}, "status": {"type": "string"},
                    "assignee": {"type": "string"}, "publish_date": {"type": "string"},
                }}, "default": []},
                "view": {"type": "string", "title": "视图", "enum": ["calendar", "timeline", "list"], "default": "calendar"},
            },
        }


class FunnelComponent(Component):
    """转化漏斗组件"""

    def __init__(
        self,
        stages: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.FUNNEL,
            id=id, title=title, description=description,
            visible=visible, order=order,
            stages=stages or [],
        )
        self.stages = stages or []

    def get_data(self) -> dict[str, Any]:
        return {"stages": self.stages}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "stages": {"type": "array", "title": "漏斗阶段", "items": {"type": "object", "properties": {
                    "name": {"type": "string"}, "count": {"type": "integer"},
                    "conversion_rate": {"type": "number"}, "drop_reason": {"type": "string"},
                }}, "default": []},
            },
        }


class ExperimentComponent(Component):
    """实验记录组件"""

    def __init__(
        self,
        hypothesis: str = "",
        variables: dict[str, str] = None,
        method: str = "",
        data_collection: str = "",
        conclusion: str = "",
        iterations: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.EXPERIMENT,
            id=id, title=title, description=description,
            visible=visible, order=order,
            hypothesis=hypothesis, variables=variables or {},
            method=method, data_collection=data_collection,
            conclusion=conclusion, iterations=iterations or [],
        )
        self.hypothesis = hypothesis
        self.variables = variables or {}
        self.method = method
        self.data_collection = data_collection
        self.conclusion = conclusion
        self.iterations = iterations or []

    def get_data(self) -> dict[str, Any]:
        return {"hypothesis": self.hypothesis, "variables": self.variables,
                "method": self.method, "data_collection": self.data_collection,
                "conclusion": self.conclusion, "iterations": self.iterations}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "hypothesis": {"type": "string", "title": "假设", "default": ""},
                "variables": {"type": "object", "title": "变量定义", "default": {}},
                "method": {"type": "string", "title": "方法", "default": ""},
                "data_collection": {"type": "string", "title": "数据收集", "default": ""},
                "conclusion": {"type": "string", "title": "结论", "default": ""},
                "iterations": {"type": "array", "title": "迭代记录", "items": {"type": "object"}, "default": []},
            },
            "required": ["hypothesis"],
        }
