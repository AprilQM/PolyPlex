"""
基础内容组件 - 文本块、图片集、视频嵌入、音频播放器、文件仓库、附件列表
"""
from typing import Any, Optional
from .base import Component, ComponentType


class TextBlockComponent(Component):
    """文本块组件 - 支持多种子类型：标题/段落/引用/代码块/提示框/折叠面板"""

    def __init__(
        self,
        content: str = "",
        sub_type: str = "paragraph",
        level: int = 2,
        author: str = "",
        source: str = "",
        language: str = "python",
        show_line_numbers: bool = True,
        placeholder: str = "",
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.TEXT_BLOCK,
            id=id, title=title, description=description,
            visible=visible, order=order,
            content=content, sub_type=sub_type, level=level,
            author=author, source=source, language=language,
            show_line_numbers=show_line_numbers, placeholder=placeholder,
        )
        self.content = content
        self.sub_type = sub_type
        self.level = level
        self.author = author
        self.source = source
        self.language = language
        self.show_line_numbers = show_line_numbers
        self.placeholder = placeholder

    def get_data(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "sub_type": self.sub_type,
            "level": self.level,
            "author": self.author,
            "source": self.source,
            "language": self.language,
            "show_line_numbers": self.show_line_numbers,
            "placeholder": self.placeholder,
        }

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {"type": "string", "title": "内容", "default": ""},
                "sub_type": {
                    "type": "string", "title": "子类型",
                    "enum": ["heading", "paragraph", "quote", "code_block", "alert", "collapse"],
                    "default": "paragraph",
                },
                "level": {"type": "integer", "title": "标题级别", "minimum": 1, "maximum": 6, "default": 2},
                "author": {"type": "string", "title": "作者", "default": ""},
                "source": {"type": "string", "title": "来源", "default": ""},
                "language": {"type": "string", "title": "代码语言", "default": "python"},
                "show_line_numbers": {"type": "boolean", "title": "显示行号", "default": True},
                "placeholder": {"type": "string", "title": "占位符", "default": ""},
            },
            "required": ["content", "sub_type"],
        }


class ImageGalleryComponent(Component):
    """图片集组件"""

    def __init__(
        self,
        images: list[dict[str, Any]] = None,
        layout: str = "grid",
        columns: int = 3,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.IMAGE_GALLERY,
            id=id, title=title, description=description,
            visible=visible, order=order,
            images=images or [], layout=layout, columns=columns,
        )
        self.images = images or []
        self.layout = layout
        self.columns = columns

    def get_data(self) -> dict[str, Any]:
        return {"images": self.images, "layout": self.layout, "columns": self.columns}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "images": {
                    "type": "array", "title": "图片列表",
                    "items": {"type": "object", "properties": {
                        "url": {"type": "string"}, "alt": {"type": "string"},
                        "caption": {"type": "string"}, "width": {"type": "integer"},
                        "height": {"type": "integer"},
                    }}, "default": [],
                },
                "layout": {"type": "string", "title": "布局", "enum": ["grid", "carousel", "masonry"], "default": "grid"},
                "columns": {"type": "integer", "title": "列数", "minimum": 1, "maximum": 6, "default": 3},
            },
        }


class VideoEmbedComponent(Component):
    """视频嵌入组件"""

    def __init__(
        self,
        url: str = "",
        platform: str = "youtube",
        poster: str = "",
        autoplay: bool = False,
        loop: bool = False,
        controls: bool = True,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.VIDEO_EMBED,
            id=id, title=title, description=description,
            visible=visible, order=order,
            url=url, platform=platform, poster=poster,
            autoplay=autoplay, loop=loop, controls=controls,
        )
        self.url = url
        self.platform = platform
        self.poster = poster
        self.autoplay = autoplay
        self.loop = loop
        self.controls = controls

    def get_data(self) -> dict[str, Any]:
        return {"url": self.url, "platform": self.platform, "poster": self.poster,
                "autoplay": self.autoplay, "loop": self.loop, "controls": self.controls}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "title": "视频URL", "default": ""},
                "platform": {"type": "string", "title": "平台", "enum": ["youtube", "bilibili", "local", "other"], "default": "youtube"},
                "poster": {"type": "string", "title": "封面图", "default": ""},
                "autoplay": {"type": "boolean", "title": "自动播放", "default": False},
                "loop": {"type": "boolean", "title": "循环播放", "default": False},
                "controls": {"type": "boolean", "title": "显示控制条", "default": True},
            },
            "required": ["url"],
        }


class AudioPlayerComponent(Component):
    """音频播放器组件"""

    def __init__(
        self,
        url: str = "",
        artist: str = "",
        cover_url: str = "",
        autoplay: bool = False,
        loop: bool = False,
        controls: bool = True,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.AUDIO_PLAYER,
            id=id, title=title, description=description,
            visible=visible, order=order,
            url=url, artist=artist, cover_url=cover_url,
            autoplay=autoplay, loop=loop, controls=controls,
        )
        self.url = url
        self.artist = artist
        self.cover_url = cover_url
        self.autoplay = autoplay
        self.loop = loop
        self.controls = controls

    def get_data(self) -> dict[str, Any]:
        return {"url": self.url, "artist": self.artist, "cover_url": self.cover_url,
                "autoplay": self.autoplay, "loop": self.loop, "controls": self.controls}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "title": "音频URL", "default": ""},
                "artist": {"type": "string", "title": "艺术家", "default": ""},
                "cover_url": {"type": "string", "title": "封面图", "default": ""},
                "autoplay": {"type": "boolean", "title": "自动播放", "default": False},
                "loop": {"type": "boolean", "title": "循环播放", "default": False},
                "controls": {"type": "boolean", "title": "显示控制条", "default": True},
            },
            "required": ["url"],
        }


class FileRepoComponent(Component):
    """文件仓库组件"""

    def __init__(
        self,
        package_id: Optional[int] = None,
        files: list[dict[str, Any]] = None,
        allow_upload: bool = True,
        allow_download: bool = True,
        allow_delete: bool = True,
        show_preview: bool = True,
        max_file_size: Optional[int] = None,
        allowed_extensions: list[str] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.FILE_REPO,
            id=id, title=title, description=description,
            visible=visible, order=order,
            package_id=package_id, files=files or [],
            allow_upload=allow_upload, allow_download=allow_download,
            allow_delete=allow_delete, show_preview=show_preview,
            max_file_size=max_file_size, allowed_extensions=allowed_extensions or [],
        )
        self.package_id = package_id
        self.files = files or []
        self.allow_upload = allow_upload
        self.allow_download = allow_download
        self.allow_delete = allow_delete
        self.show_preview = show_preview
        self.max_file_size = max_file_size
        self.allowed_extensions = allowed_extensions or []

    def get_data(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id, "files": self.files,
            "allow_upload": self.allow_upload, "allow_download": self.allow_download,
            "allow_delete": self.allow_delete, "show_preview": self.show_preview,
            "max_file_size": self.max_file_size, "allowed_extensions": self.allowed_extensions,
        }

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "package_id": {"type": ["integer", "null"], "title": "文件包ID", "default": None},
                "files": {"type": "array", "title": "文件列表", "items": {"type": "object"}, "default": []},
                "allow_upload": {"type": "boolean", "title": "允许上传", "default": True},
                "allow_download": {"type": "boolean", "title": "允许下载", "default": True},
                "allow_delete": {"type": "boolean", "title": "允许删除", "default": True},
                "show_preview": {"type": "boolean", "title": "显示预览", "default": True},
                "max_file_size": {"type": ["integer", "null"], "title": "最大文件大小", "default": None},
                "allowed_extensions": {"type": "array", "title": "允许的扩展名", "items": {"type": "string"}, "default": []},
            },
        }


class AttachmentListComponent(Component):
    """附件列表组件"""

    def __init__(
        self,
        attachments: list[dict[str, Any]] = None,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.ATTACHMENT_LIST,
            id=id, title=title, description=description,
            visible=visible, order=order,
            attachments=attachments or [],
        )
        self.attachments = attachments or []

    def get_data(self) -> dict[str, Any]:
        return {"attachments": self.attachments}

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "attachments": {
                    "type": "array", "title": "附件列表",
                    "items": {"type": "object", "properties": {
                        "uuid": {"type": "string"}, "filename": {"type": "string"},
                        "file_size": {"type": "integer"}, "file_type": {"type": "string"},
                    }}, "default": [],
                }
            },
        }


class GitRepoComponent(Component):
    """代码仓库组件 - 关联一个 Git 仓库"""

    def __init__(
        self,
        description: str = "",
        default_branch: str = "master",
        id: Optional[str] = None,
        title: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
    ):
        super().__init__(
            component_type=ComponentType.GIT_REPO,
            id=id, title=title, description=description,
            visible=visible, order=order,
            default_branch=default_branch,
        )
        self.default_branch = default_branch

    def get_data(self) -> dict[str, Any]:
        return {
            "description": self.description or "",
            "default_branch": self.default_branch,
        }

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "description": {"type": "string", "title": "仓库描述", "default": ""},
                "default_branch": {"type": "string", "title": "默认分支", "default": "master"},
            },
        }
