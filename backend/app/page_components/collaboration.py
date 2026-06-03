"""
协作组件 - 评论锚点、投票模块、任务指派卡、变更日志
"""
from typing import Any, Optional
from .base import Component, ComponentType


class CommentAnchorComponent(Component):
    """评论锚点组件"""

    def __init__(
        self,
        comments: list[dict[str, Any]] = None,
        allow_comment: bool = True,
        placeholder: str = "发表评论...",
        max_length: int = 1000,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.COMMENT_ANCHOR,
            id=id, title=title, description=description,
            visible=visible, order=order,
            comments=comments or [], allow_comment=allow_comment,
            placeholder=placeholder, max_length=max_length,
        )
        self.comments = comments or []
        self.allow_comment = allow_comment
        self.placeholder = placeholder
        self.max_length = max_length

    def get_data(self) -> dict[str, Any]:
        return {"comments": self.comments, "allow_comment": self.allow_comment,
                "placeholder": self.placeholder, "max_length": self.max_length}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "comments": {"type": "array", "title": "评论列表", "items": {"type": "object"}, "default": []},
                "allow_comment": {"type": "boolean", "title": "允许评论", "default": True},
                "placeholder": {"type": "string", "title": "占位符", "default": "发表评论..."},
                "max_length": {"type": "integer", "title": "最大长度", "default": 1000},
            },
        }


class VoteModuleComponent(Component):
    """投票模块组件"""

    def __init__(
        self,
        question: str = "",
        options: list[dict[str, Any]] = None,
        vote_type: str = "single",
        anonymous: bool = False,
        show_result: bool = False,
        end_time: Optional[int] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.VOTE_MODULE,
            id=id, title=title, description=description,
            visible=visible, order=order,
            question=question, options=options or [],
            vote_type=vote_type, anonymous=anonymous,
            show_result=show_result, end_time=end_time,
        )
        self.question = question
        self.options = options or []
        self.vote_type = vote_type
        self.anonymous = anonymous
        self.show_result = show_result
        self.end_time = end_time

    def get_data(self) -> dict[str, Any]:
        return {"question": self.question, "options": self.options, "vote_type": self.vote_type,
                "anonymous": self.anonymous, "show_result": self.show_result, "end_time": self.end_time}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "question": {"type": "string", "title": "投票问题", "default": ""},
                "options": {"type": "array", "title": "选项", "items": {"type": "object", "properties": {
                    "text": {"type": "string"}, "count": {"type": "integer"},
                }}, "default": []},
                "vote_type": {"type": "string", "title": "投票类型", "enum": ["single", "multiple", "rank"], "default": "single"},
                "anonymous": {"type": "boolean", "title": "匿名投票", "default": False},
                "show_result": {"type": "boolean", "title": "显示结果", "default": False},
                "end_time": {"type": ["integer", "null"], "title": "截止时间", "default": None},
            },
            "required": ["question", "options"],
        }


class TaskAssignComponent(Component):
    """任务指派卡组件"""

    def __init__(
        self,
        assignee: str = "",
        due_date: str = "",
        priority: str = "medium",
        status: str = "pending",
        description_text: str = "",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.TASK_ASSIGN,
            id=id, title=title, description=description,
            visible=visible, order=order,
            assignee=assignee, due_date=due_date, priority=priority,
            status=status, description_text=description_text,
        )
        self.assignee = assignee
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.description_text = description_text

    def get_data(self) -> dict[str, Any]:
        return {"assignee": self.assignee, "due_date": self.due_date, "priority": self.priority,
                "status": self.status, "description": self.description_text}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "assignee": {"type": "string", "title": "负责人", "default": ""},
                "due_date": {"type": "string", "title": "截止日期", "default": ""},
                "priority": {"type": "string", "title": "优先级", "enum": ["low", "medium", "high", "urgent"], "default": "medium"},
                "status": {"type": "string", "title": "状态", "enum": ["pending", "in_progress", "completed", "blocked"], "default": "pending"},
                "description": {"type": "string", "title": "任务描述", "default": ""},
            },
            "required": ["assignee"],
        }


class ChangelogComponent(Component):
    """变更日志组件"""

    def __init__(
        self,
        entries: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.CHANGELOG,
            id=id, title=title, description=description,
            visible=visible, order=order,
            entries=entries or [],
        )
        self.entries = entries or []

    def get_data(self) -> dict[str, Any]:
        return {"entries": self.entries}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "entries": {"type": "array", "title": "变更条目", "items": {"type": "object", "properties": {
                    "version": {"type": "string"}, "date": {"type": "string"},
                    "type": {"type": "string", "enum": ["added", "modified", "fixed", "deprecated", "security"]},
                    "description": {"type": "string"}, "author": {"type": "string"},
                }}, "default": []},
            },
        }
