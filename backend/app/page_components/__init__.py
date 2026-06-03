"""
页面组件库 - 全部48个组件，8大分类
"""
from .base import Component, ComponentType, PageTemplate

# 基础内容（6）
from .basic import (
    TextBlockComponent,
    ImageGalleryComponent,
    VideoEmbedComponent,
    AudioPlayerComponent,
    FileRepoComponent,
    AttachmentListComponent,
    GitRepoComponent,
)

# 结构化（5）
from .structured import (
    TableComponent,
    KanbanComponent,
    TimelineComponent,
    StepsComponent,
    ListComponent,
)

# 可视化（6）
from .visualization import (
    MindmapComponent,
    FlowchartComponent,
    RelationGraphComponent,
    DataChartComponent,
    MoodboardComponent,
    WhiteboardComponent,
)

# 数据与度量（5）
from .metric import (
    MetricCardComponent,
    ProgressBarComponent,
    CounterComponent,
    ScorecardComponent,
    FormulaComponent,
)

# 协作（4）
from .collaboration import (
    CommentAnchorComponent,
    VoteModuleComponent,
    TaskAssignComponent,
    ChangelogComponent,
)

# 引用与关联（4）
from .reference import (
    PageRefComponent,
    EmbedViewComponent,
    BreadcrumbComponent,
    TagSetComponent,
)

# 领域专用（13）
from .domain_specific import (
    BizCanvasComponent,
    PersonaCardComponent,
    SwotComponent,
    CompeteMatrixComponent,
    StoryTreeComponent,
    CharacterCardComponent,
    ChapterTableComponent,
    StoryboardComponent,
    LevelDesignComponent,
    CourseOutlineComponent,
    ContentCalendarComponent,
    FunnelComponent,
    ExperimentComponent,
)

# 通用功能（5）
from .utility import (
    DividerComponent,
    SpacerComponent,
    MultiColumnComponent,
    TabsComponent,
    AnchorTocComponent,
)

__all__ = [
    # 基类
    "Component", "ComponentType", "PageTemplate",

    # 基础内容
    "TextBlockComponent", "ImageGalleryComponent", "VideoEmbedComponent",
    "AudioPlayerComponent", "FileRepoComponent", "AttachmentListComponent",
    "GitRepoComponent",

    # 结构化
    "TableComponent", "KanbanComponent", "TimelineComponent",
    "StepsComponent", "ListComponent",

    # 可视化
    "MindmapComponent", "FlowchartComponent", "RelationGraphComponent",
    "DataChartComponent", "MoodboardComponent", "WhiteboardComponent",

    # 数据与度量
    "MetricCardComponent", "ProgressBarComponent", "CounterComponent",
    "ScorecardComponent", "FormulaComponent",

    # 协作
    "CommentAnchorComponent", "VoteModuleComponent", "TaskAssignComponent",
    "ChangelogComponent",

    # 引用与关联
    "PageRefComponent", "EmbedViewComponent", "BreadcrumbComponent",
    "TagSetComponent",

    # 领域专用
    "BizCanvasComponent", "PersonaCardComponent", "SwotComponent",
    "CompeteMatrixComponent", "StoryTreeComponent", "CharacterCardComponent",
    "ChapterTableComponent", "StoryboardComponent", "LevelDesignComponent",
    "CourseOutlineComponent", "ContentCalendarComponent", "FunnelComponent",
    "ExperimentComponent",

    # 通用功能
    "DividerComponent", "SpacerComponent", "MultiColumnComponent",
    "TabsComponent", "AnchorTocComponent",
]
