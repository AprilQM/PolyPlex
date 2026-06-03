"""
写作领域页面模板 - 使用组件构建
"""
from app.page_components import (
    PageTemplate,
    TextBlockComponent, ImageGalleryComponent,
    TableComponent, KanbanComponent, TimelineComponent, StepsComponent, ListComponent,
    MindmapComponent, FlowchartComponent, RelationGraphComponent, DataChartComponent, MoodboardComponent, WhiteboardComponent,
    MetricCardComponent, ProgressBarComponent, CounterComponent, ScorecardComponent, FormulaComponent,
    CommentAnchorComponent, VoteModuleComponent, TaskAssignComponent,
    PageRefComponent, EmbedViewComponent, TagSetComponent,
    DividerComponent, SpacerComponent, MultiColumnComponent, TabsComponent,
    StoryTreeComponent, CharacterCardComponent,
)


class WritingPages:
    """写作领域页面模板"""

    @staticmethod
    def _create_story_tree_components() -> list:
        """创建故事结构树页面的组件列表"""
        template = PageTemplate(
            name="story_tree",
            display_name="故事结构树",
            icon="tree",
            category="writing",
            description="故事分支结构和多线叙事规划",
        )

        template.add_component(TextBlockComponent(
            id="story_tree_title",
            content="故事结构树",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="story_tree_desc",
            content="规划故事的多线叙事结构和分支走向，梳理情节脉络。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(StoryTreeComponent(
            id="story_sections",
            nodes=[
                {"id": "act_1", "title": "第一幕：开端", "summary": "主角登场，世界观建立", "parent_id": None, "level": 1, "status": "draft"},
                {"id": "ch_1", "title": "第一章", "summary": "日常被打破", "parent_id": "act_1", "level": 2, "status": "draft"},
                {"id": "ch_2", "title": "第二章", "summary": "收到神秘邀请", "parent_id": "act_1", "level": 2, "status": "draft"},
                {"id": "act_2", "title": "第二幕：冲突", "summary": "矛盾升级，危机浮现", "parent_id": None, "level": 1, "status": "draft"},
                {"id": "ch_3", "title": "第三章", "summary": "初次交锋", "parent_id": "act_2", "level": 2, "status": "draft"},
            ],
            order=3,
        ))

        template.add_component(MindmapComponent(
            id="story_mindmap",
            nodes=[
                {"id": "root", "label": "故事", "children": ["act1", "act2", "act3"], "parent": None},
                {"id": "act1", "label": "开端", "children": ["ch1", "ch2"], "parent": "root"},
                {"id": "act2", "label": "发展", "children": ["ch3", "ch4"], "parent": "root"},
                {"id": "act3", "label": "高潮", "children": ["ch5", "ch6"], "parent": "root"},
                {"id": "ch1", "label": "平凡日常", "children": [], "parent": "act1"},
                {"id": "ch2", "label": "转折事件", "children": [], "parent": "act1"},
                {"id": "ch3", "label": "深入探索", "children": [], "parent": "act2"},
                {"id": "ch4", "label": "危机浮现", "children": [], "parent": "act2"},
                {"id": "ch5", "label": "最终对决", "children": [], "parent": "act3"},
                {"id": "ch6", "label": "结局", "children": [], "parent": "act3"},
            ],
            layout="tree",
            order=4,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_character_card_components() -> list:
        """创建角色卡片页面的组件列表"""
        template = PageTemplate(
            name="character_card",
            display_name="角色卡片",
            icon="person",
            category="writing",
            description="角色详细信息管理",
        )

        template.add_component(TextBlockComponent(
            id="character_card_title",
            content="角色卡片",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="character_card_desc",
            content="管理和记录故事角色的详细信息、背景和关系。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(CharacterCardComponent(
            id="main_character",
            name="主角姓名",
            order=3,
        ))

        template.add_component(TableComponent(
            id="character_details",
            columns=[
                {"key": "name", "title": "角色名", "width": "20%"},
                {"key": "role", "title": "定位", "width": "15%"},
                {"key": "age", "title": "年龄", "width": "10%"},
                {"key": "trait", "title": "性格特征", "width": "30%"},
                {"key": "arc", "title": "成长弧线", "width": "25%"},
            ],
            data=[
                {"name": "主角", "role": "主人公", "age": "25", "trait": "勇敢、善良、冲动", "arc": "从平凡到英雄"},
                {"name": "配角 A", "role": "挚友", "age": "26", "trait": "幽默、忠诚", "arc": "支持主角成长"},
                {"name": "反派", "role": " antagonist", "age": "40", "trait": "深沉、野心", "arc": "从盟友到敌人"},
                {"name": "配角 B", "role": "导师", "age": "60", "trait": "智慧、神秘", "arc": "传授知识后隐退"},
            ],
            order=4,
        ))

        template.add_component(ListComponent(
            id="character_relations",
            items=[
                {"label": "主角", "value": "protagonist", "description": "与配角 A 是挚友，与反派曾是师徒", "icon": "link"},
                {"label": "配角 A", "value": "sidekick", "description": "从小与主角一起长大", "icon": "link"},
                {"label": "反派", "value": "antagonist", "description": "曾是主角的导师", "icon": "link"},
            ],
            list_type="definition",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_world_setting_components() -> list:
        """创建世界观设定页面的组件列表"""
        template = PageTemplate(
            name="world_setting",
            display_name="世界观设定",
            icon="globe",
            category="writing",
            description="故事世界观和背景设定",
        )

        template.add_component(TextBlockComponent(
            id="world_setting_title",
            content="世界观设定",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="world_setting_desc",
            content="构建故事的世界观体系，包括地理、历史、文化、魔法/科技系统等。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TextBlockComponent(
            id="world_geography",
            content="地理环境描述：故事发生的世界由三块大陆组成，中央是繁华的王国，北方是冰雪覆盖的荒原，南方是神秘的群岛。每个区域都有独特的生态系统和文化特征。",
            sub_type="paragraph",
            order=3,
        ))

        template.add_component(TextBlockComponent(
            id="world_history",
            content="历史背景：千年前，上古文明因一场大灾变而陨落，留下了散布在世界各地的遗迹。如今的文明在废墟上重建，古老的秘密逐渐被揭开。",
            sub_type="paragraph",
            order=4,
        ))

        template.add_component(MindmapComponent(
            id="world_mindmap",
            nodes=[
                {"id": "world", "label": "世界观", "children": ["geo", "history", "magic", "culture"], "parent": None},
                {"id": "geo", "label": "地理", "children": ["north", "central", "south"], "parent": "world"},
                {"id": "history", "label": "历史", "children": ["ancient", "modern"], "parent": "world"},
                {"id": "magic", "label": "魔法系统", "children": ["elements", "rules"], "parent": "world"},
                {"id": "culture", "label": "文化", "children": ["religion", "customs"], "parent": "world"},
                {"id": "north", "label": "北方冻土", "children": [], "parent": "geo"},
                {"id": "central", "label": "中央王国", "children": [], "parent": "geo"},
                {"id": "south", "label": "南方群岛", "children": [], "parent": "geo"},
                {"id": "ancient", "label": "上古时代", "children": [], "parent": "history"},
                {"id": "modern", "label": "当今纪元", "children": [], "parent": "history"},
                {"id": "elements", "label": "元素体系", "children": [], "parent": "magic"},
                {"id": "rules", "label": "规则限制", "children": [], "parent": "magic"},
                {"id": "religion", "label": "宗教信仰", "children": [], "parent": "culture"},
                {"id": "customs", "label": "风俗习惯", "children": [], "parent": "culture"},
            ],
            layout="radial",
            order=5,
        ))

        template.add_component(ImageGalleryComponent(
            id="world_images",
            images=[
                {"url": "", "caption": "世界地图概念图", "alt": "world_map_concept"},
                {"url": "", "caption": "城市风貌参考", "alt": "city_reference"},
            ],
            layout="grid",
            columns=2,
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_chapter_table_components() -> list:
        """创建章节规划表页面的组件列表"""
        template = PageTemplate(
            name="chapter_table",
            display_name="章节规划表",
            icon="table",
            category="writing",
            description="分章节详细规划和大纲",
        )

        template.add_component(TextBlockComponent(
            id="chapter_table_title",
            content="章节规划表",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="chapter_table_desc",
            content="以表格形式规划每个章节的内容、进度和状态。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="chapter_table",
            columns=[
                {"key": "chapter", "title": "章节", "width": "15%"},
                {"key": "title", "title": "标题", "width": "20%"},
                {"key": "summary", "title": "内容概要", "width": "30%"},
                {"key": "word_count", "title": "预计字数", "width": "15%"},
                {"key": "status", "title": "状态", "width": "20%"},
            ],
            data=[
                {"chapter": "第一章", "title": "命运的转折", "summary": "主角在平凡生活中遇到改变一生的事件", "word_count": "5000", "status": "已完成"},
                {"chapter": "第二章", "title": "新的世界", "summary": "主角踏入未知领域，结识新伙伴", "word_count": "6000", "status": "写作中"},
                {"chapter": "第三章", "title": "暗流涌动", "summary": "隐藏在表面下的危机开始显现", "word_count": "5500", "status": "待开始"},
                {"chapter": "第四章", "title": "抉择时刻", "summary": "主角面临关键选择", "word_count": "6000", "status": "待开始"},
                {"chapter": "第五章", "title": "高潮对决", "summary": "与反派的正面交锋", "word_count": "8000", "status": "待开始"},
            ],
            order=3,
        ))

        template.add_component(ListComponent(
            id="chapter_notes",
            items=[
                {"label": "已完成", "value": "done", "description": "1 章", "icon": "check"},
                {"label": "写作中", "value": "writing", "description": "1 章", "icon": "edit"},
                {"label": "待开始", "value": "todo", "description": "3 章", "icon": "clock"},
            ],
            list_type="sorted",
            order=4,
        ))

        template.add_component(ProgressBarComponent(
            id="chapter_progress",
            percentage=20.0,
            style="bar",
            color="blue",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_dialogue_board_components() -> list:
        """创建对话板页面的组件列表"""
        template = PageTemplate(
            name="dialogue_board",
            display_name="对话板",
            icon="chat",
            category="writing",
            description="角色对话设计和编排",
        )

        template.add_component(TextBlockComponent(
            id="dialogue_board_title",
            content="对话板",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="dialogue_board_desc",
            content="设计和编排角色之间的对话场景，把握人物语气和情感。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(KanbanComponent(
            id="dialogue_kanban",
            columns=[
                {"id": "planned", "title": "待编写", "color": "gray"},
                {"id": "writing", "title": "编写中", "color": "blue"},
                {"id": "review", "title": "待润色", "color": "orange"},
                {"id": "done", "title": "已完成", "color": "green"},
            ],
            cards=[
                {"id": "card_1", "title": "初次相遇对话", "description": "主角与配角的第一次对话", "column_id": "done"},
                {"id": "card_2", "title": "争执场景", "description": "主角与反派的对峙", "column_id": "review"},
                {"id": "card_3", "title": "告白场景", "description": "主角与恋人的感情戏", "column_id": "writing"},
                {"id": "card_4", "title": "最终决战对话", "description": "结局前的重要对话", "column_id": "planned"},
            ],
            order=3,
        ))

        template.add_component(TableComponent(
            id="dialogue_lines",
            columns=[
                {"key": "scene", "title": "场景", "width": "15%"},
                {"key": "speaker", "title": "说话人", "width": "15%"},
                {"key": "line", "title": "台词", "width": "50%"},
                {"key": "emotion", "title": "情感", "width": "20%"},
            ],
            data=[
                {"scene": "初次相遇", "speaker": "主角", "line": "你是谁？为什么会在这里？", "emotion": "警惕"},
                {"scene": "初次相遇", "speaker": "配角", "line": "这个问题应该由我来问。", "emotion": "冷静"},
                {"scene": "争执", "speaker": "反派", "line": "你根本不了解真相。", "emotion": "愤怒"},
                {"scene": "争执", "speaker": "主角", "line": "那就告诉我真相！", "emotion": "激动"},
            ],
            order=4,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_submission_tracker_components() -> list:
        """创建投稿追踪页面的组件列表"""
        template = PageTemplate(
            name="submission_tracker",
            display_name="投稿追踪",
            icon="send",
            category="writing",
            description="投稿进度和反馈追踪",
        )

        template.add_component(TextBlockComponent(
            id="submission_tracker_title",
            content="投稿追踪",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="submission_tracker_desc",
            content="追踪稿件投递进度、评审状态和反馈意见。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(MetricCardComponent(
            id="submission_metrics",
            value="5",
            label="总投稿数",
            prefix="",
            suffix="篇",
            trend="+2",
            size="medium",
            order=3,
        ))

        template.add_component(TableComponent(
            id="submission_table",
            columns=[
                {"key": "title", "title": "作品名", "width": "20%"},
                {"key": "target", "title": "投稿目标", "width": "20%"},
                {"key": "date", "title": "投稿日期", "width": "15%"},
                {"key": "status", "title": "状态", "width": "15%"},
                {"key": "feedback", "title": "反馈", "width": "30%"},
            ],
            data=[
                {"title": "短篇小说 A", "target": "文学月刊", "date": "2024-01-05", "status": "已录用", "feedback": "预计下月刊出"},
                {"title": "短篇小说 B", "target": "故事会", "date": "2024-01-15", "status": "审稿中", "feedback": "初审通过"},
                {"title": "长篇节选", "target": "出版社 X", "date": "2024-02-01", "status": "待回复", "feedback": ""},
                {"title": "诗歌集", "target": "诗刊", "date": "2024-02-10", "status": "被拒", "feedback": "风格不符"},
            ],
            order=4,
        ))

        template.add_component(TimelineComponent(
            id="submission_timeline",
            events=[
                {"id": "evt_1", "title": "短篇小说 A 投稿", "description": "投稿至文学月刊", "date": "2024-01-05", "icon": "send"},
                {"id": "evt_2", "title": "短篇小说 A 录用", "description": "收到录用通知", "date": "2024-01-20", "icon": "check"},
                {"id": "evt_3", "title": "短篇小说 B 投稿", "description": "投稿至故事会", "date": "2024-01-15", "icon": "send"},
                {"id": "evt_4", "title": "长篇节选投稿", "description": "投稿至出版社 X", "date": "2024-02-01", "icon": "send"},
            ],
            layout="vertical",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_idea_collection_components() -> list:
        """创建灵感收集页面的组件列表"""
        template = PageTemplate(
            name="idea_collection",
            display_name="灵感收集",
            icon="bulb",
            category="writing",
            description="收集和整理创作灵感",
        )

        template.add_component(TextBlockComponent(
            id="idea_collection_title",
            content="灵感收集",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="idea_collection_desc",
            content="记录灵光一现的创意，分类管理创作灵感。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(ListComponent(
            id="idea_list",
            items=[
                {"label": "反转结局构思", "value": "idea_1", "description": "看似反派的角色其实是隐藏的保护者", "icon": "lightbulb", "checked": False},
                {"label": "特殊能力设定", "value": "idea_2", "description": "以记忆为媒介的魔法体系", "icon": "lightbulb", "checked": True},
                {"label": "故事开头灵感", "value": "idea_3", "description": "主角在梦中得到预知能力", "icon": "lightbulb", "checked": False},
                {"label": "角色关系设计", "value": "idea_4", "description": "失散多年的兄妹在不同阵营相遇", "icon": "lightbulb", "checked": False},
                {"label": "场景灵感", "value": "idea_5", "description": "在雨中进行的决斗场景", "icon": "lightbulb", "checked": True},
            ],
            list_type="simple",
            show_checkbox=True,
            order=3,
        ))

        template.add_component(TagSetComponent(
            id="idea_tags",
            tags=[
                {"name": "剧情", "color": "blue", "count": 3},
                {"name": "角色", "color": "green", "count": 2},
                {"name": "世界观", "color": "purple", "count": 1},
                {"name": "场景", "color": "orange", "count": 1},
            ],
            allow_create=True,
            order=4,
        ))

        template.add_component(TextBlockComponent(
            id="idea_detail",
            content="详细描述：",
            sub_type="paragraph",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_reference_table_components() -> list:
        """创建参考资料表页面的组件列表"""
        template = PageTemplate(
            name="reference_table",
            display_name="参考资料表",
            icon="bookmark",
            category="writing",
            description="创作参考和资料管理",
        )

        template.add_component(TextBlockComponent(
            id="reference_table_title",
            content="参考资料表",
            sub_type="heading",
            level=1,
            order=0,
        ))

        template.add_component(TextBlockComponent(
            id="reference_table_desc",
            content="管理创作过程中用到的参考资料、考据和文献。",
            sub_type="paragraph",
            order=1,
        ))

        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="reference_table",
            columns=[
                {"key": "title", "title": "资料名", "width": "25%"},
                {"key": "type", "title": "类型", "width": "15%"},
                {"key": "source", "title": "来源", "width": "20%"},
                {"key": "relevance", "title": "相关章节", "width": "20%"},
                {"key": "notes", "title": "备注", "width": "20%"},
            ],
            data=[
                {"title": "中世纪建筑图鉴", "type": "书籍", "source": "图书馆借阅", "relevance": "场景描写", "notes": "城堡描写参考"},
                {"title": "古代兵器百科", "type": "网站", "source": "知乎专栏", "relevance": "战斗描写", "notes": "剑术参考"},
                {"title": "XX 地民俗志", "type": "论文", "source": "知网", "relevance": "世界观", "notes": "风俗文化参考"},
                {"title": "星座神话集", "type": "书籍", "source": "个人收藏", "relevance": "设定灵感", "notes": "魔法体系来源"},
            ],
            order=3,
        ))

        template.add_component(TagSetComponent(
            id="reference_tags",
            tags=[
                {"name": "书籍", "color": "blue", "count": 2},
                {"name": "网站", "color": "green", "count": 1},
                {"name": "论文", "color": "purple", "count": 1},
            ],
            allow_create=True,
            order=4,
        ))

        template.add_component(PageRefComponent(
            id="reference_link",
            ref_type="link",
            display_title="查看相关角色卡片",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    # PAGE_TYPES 字典
    PAGE_TYPES = {
        "story_tree": {
            "name": "story_tree",
            "display_name": "故事结构树",
            "icon": "tree",
            "category": "writing",
            "description": "故事分支结构和多线叙事规划",
            "default_schema": {
                "components": _create_story_tree_components.__func__(),
            }
        },
        "character_card": {
            "name": "character_card",
            "display_name": "角色卡片",
            "icon": "person",
            "category": "writing",
            "description": "角色详细信息管理",
            "default_schema": {
                "components": _create_character_card_components.__func__(),
            }
        },
        "world_setting": {
            "name": "world_setting",
            "display_name": "世界观设定",
            "icon": "globe",
            "category": "writing",
            "description": "故事世界观和背景设定",
            "default_schema": {
                "components": _create_world_setting_components.__func__(),
            }
        },
        "chapter_table": {
            "name": "chapter_table",
            "display_name": "章节规划表",
            "icon": "table",
            "category": "writing",
            "description": "分章节详细规划和大纲",
            "default_schema": {
                "components": _create_chapter_table_components.__func__(),
            }
        },
        "dialogue_board": {
            "name": "dialogue_board",
            "display_name": "对话板",
            "icon": "chat",
            "category": "writing",
            "description": "角色对话设计和编排",
            "default_schema": {
                "components": _create_dialogue_board_components.__func__(),
            }
        },
        "submission_tracker": {
            "name": "submission_tracker",
            "display_name": "投稿追踪",
            "icon": "send",
            "category": "writing",
            "description": "投稿进度和反馈追踪",
            "default_schema": {
                "components": _create_submission_tracker_components.__func__(),
            }
        },
        "idea_collection": {
            "name": "idea_collection",
            "display_name": "灵感收集",
            "icon": "bulb",
            "category": "writing",
            "description": "收集和整理创作灵感",
            "default_schema": {
                "components": _create_idea_collection_components.__func__(),
            }
        },
        "reference_table": {
            "name": "reference_table",
            "display_name": "参考资料表",
            "icon": "bookmark",
            "category": "writing",
            "description": "创作参考和资料管理",
            "default_schema": {
                "components": _create_reference_table_components.__func__(),
            }
        },
    }
