"""
组件基类定义 - 包含所有48种组件类型的枚举
"""
from abc import ABC, abstractmethod
from typing import Any, Optional
from enum import Enum


class ComponentType(str, Enum):
    """组件类型枚举 - 共48种，分为8大类"""

    # ========== 一、基础内容组件 (6) ==========
    TEXT_BLOCK = "text_block"              # 文本块（标题/段落/引用/代码块/提示框/折叠面板）
    IMAGE_GALLERY = "image_gallery"        # 图片集
    VIDEO_EMBED = "video_embed"            # 视频嵌入
    AUDIO_PLAYER = "audio_player"          # 音频播放器
    FILE_REPO = "file_repo"                # 文件仓库
    ATTACHMENT_LIST = "attachment_list"    # 附件列表

    # ========== 二、结构化组件 (5) ==========
    TABLE = "table"                        # 表格
    KANBAN = "kanban"                      # 看板
    TIMELINE = "timeline"                  # 时间线
    STEPS = "steps"                        # 步骤条
    LIST = "list"                          # 列表

    # ========== 三、可视化组件 (6) ==========
    MINDMAP = "mindmap"                    # 思维导图
    FLOWCHART = "flowchart"                # 流程图
    RELATION_GRAPH = "relation_graph"      # 关系图
    DATA_CHART = "data_chart"              # 数据图表
    MOODBOARD = "moodboard"                # 情绪板
    WHITEBOARD = "whiteboard"              # 白板

    # ========== 四、数据与度量组件 (5) ==========
    METRIC_CARD = "metric_card"            # 指标卡
    PROGRESS_BAR = "progress_bar"          # 进度条
    COUNTER = "counter"                    # 计数器
    SCORECARD = "scorecard"                # 评分表
    FORMULA = "formula"                    # 测算公式

    # ========== 五、协作组件 (4) ==========
    COMMENT_ANCHOR = "comment_anchor"      # 评论锚点
    VOTE_MODULE = "vote_module"            # 投票模块
    TASK_ASSIGN = "task_assign"            # 任务指派卡
    CHANGELOG = "changelog"                # 变更日志

    # ========== 六、引用与关联组件 (4) ==========
    PAGE_REF = "page_ref"                  # 页面引用
    EMBED_VIEW = "embed_view"              # 嵌入视图
    BREADCRUMB = "breadcrumb"              # 面包屑导航
    TAG_SET = "tag_set"                    # 标签集

    # ========== 七、领域专用组件 (13) ==========
    BIZ_CANVAS = "biz_canvas"              # 商业画布
    PERSONA_CARD = "persona_card"          # 用户画像卡
    SWOT = "swot"                          # SWOT矩阵
    COMPETE_MATRIX = "compete_matrix"      # 竞品分析矩阵
    STORY_TREE = "story_tree"              # 故事大纲树
    CHARACTER_CARD = "character_card"      # 角色设定卡
    CHAPTER_TABLE = "chapter_table"        # 章节细纲表
    STORYBOARD = "storyboard"              # 分镜脚本板
    LEVEL_DESIGN = "level_design"          # 关卡设计文档
    COURSE_OUTLINE = "course_outline"      # 课程大纲
    CONTENT_CALENDAR = "content_calendar"  # 内容日历
    FUNNEL = "funnel"                      # 转化漏斗
    EXPERIMENT = "experiment"              # 实验记录

    # ========== 八、通用功能型组件 (5) ==========
    DIVIDER = "divider"                    # 分隔线
    SPACER = "spacer"                      # 空白占位
    MULTI_COLUMN = "multi_column"          # 多列布局
    TABS = "tabs"                          # 选项卡
    ANCHOR_TOC = "anchor_toc"              # 锚点目录

    # ========== 九、代码仓库组件 (1) ==========
    GIT_REPO = "git_repo"                  # 代码仓库（关联 Git 仓库）


class Component(ABC):
    """组件基类"""

    def __init__(
        self,
        component_type: ComponentType,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        visible: bool = True,
        order: int = 0,
        **kwargs
    ):
        self.component_type = component_type
        self.id = id
        self.title = title
        self.description = description
        self.visible = visible
        self.order = order
        self.extra_data = kwargs

    @abstractmethod
    def get_data(self) -> dict[str, Any]:
        """获取组件的数据"""
        pass

    @abstractmethod
    def get_schema(self) -> dict[str, Any]:
        """获取组件的 schema 定义"""
        pass

    def to_dict(self) -> dict[str, Any]:
        """将组件转换为字典"""
        return {
            "type": self.component_type.value,
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "visible": self.visible,
            "order": self.order,
            "data": self.get_data(),
            "schema": self.get_schema(),
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.component_type.value}, id={self.id})"


class PageTemplate:
    """页面模板基类 - 用于组合多个组件"""

    def __init__(self, name: str, display_name: str, icon: str, category: str, description: str):
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self.category = category
        self.description = description
        self.components: list[Component] = []

    def add_component(self, component: Component) -> "PageTemplate":
        """添加组件到模板"""
        self.components.append(component)
        return self

    def add_components(self, components: list[Component]) -> "PageTemplate":
        """批量添加组件到模板"""
        self.components.extend(components)
        return self

    def get_page_type_info(self) -> dict[str, Any]:
        """获取页面类型信息（兼容原有格式）"""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "icon": self.icon,
            "category": self.category,
            "description": self.description,
            "default_schema": self.get_default_schema(),
        }

    def get_default_schema(self) -> dict[str, Any]:
        """获取默认 schema - 由组件组合而成"""
        return {
            "components": [component.to_dict() for component in self.components]
        }
