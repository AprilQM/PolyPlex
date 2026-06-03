"""
媒体领域页面模板 - 分镜脚本、关卡设计、角色技能、叙事分支、场景概念、配音脚本、玩法原型
"""
from app.page_components import (
    PageTemplate,
    TextBlockComponent, ImageGalleryComponent, TableComponent, ListComponent, StepsComponent,
    FlowchartComponent, FileRepoComponent, DividerComponent, SpacerComponent,
    StoryboardComponent, LevelDesignComponent,
)


class MediaPages:
    """媒体领域页面模板"""

    @staticmethod
    def _create_storyboard_panel_components() -> list:
        template = PageTemplate(name="storyboard_panel", display_name="分镜脚本板", icon="film", category="media", description="影视分镜头脚本设计")
        template.add_component(TextBlockComponent(id="title", content="分镜脚本板", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="设计和展示影视片段的镜头脚本。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(StoryboardComponent(
            id="storyboard",
            shots=[
                {"shot_no": 1, "scene": "开场", "shot_type": "远景", "description": "建立环境氛围", "dialogue": "", "duration": 5.0, "sound": "环境音", "sketch_url": ""},
                {"shot_no": 2, "scene": "对话", "shot_type": "中景", "description": "角色对话场景", "dialogue": "台词内容", "duration": 8.0, "sound": "对话音", "sketch_url": ""},
                {"shot_no": 3, "scene": "高潮", "shot_type": "特写", "description": "关键情节揭示", "dialogue": "关键台词", "duration": 6.0, "sound": "背景乐", "sketch_url": ""},
            ],
            order=3,
        ))
        template.add_component(TextBlockComponent(id="direction_notes", content="导演备注：记录镜头衔接和视觉风格要求。", sub_type="paragraph", placeholder="镜头调度、色彩风格、转场方式等备注", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_level_design_doc_components() -> list:
        template = PageTemplate(name="level_design_doc", display_name="关卡设计文档", icon="map", category="media", description="游戏关卡设计文档")
        template.add_component(TextBlockComponent(id="title", content="关卡设计文档", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="详细设计游戏关卡的结构、机制和内容。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(LevelDesignComponent(
            id="level_design",
            level_name="示例关卡",
            theme="森林遗迹",
            difficulty="medium",
            core_mechanic="平台跳跃与解谜",
            enemies=[{"name": "守卫者", "count": 5, "behavior": "巡逻"}, {"name": "陷阱", "count": 3, "behavior": "触发"}],
            items=[{"name": "钥匙", "position": "B2区", "effect": "开门"}, {"name": "宝石", "position": "隐藏墙", "effect": "加分"}],
            clear_condition="到达终点传送门",
            order=3,
        ))
        template.add_component(TextBlockComponent(id="level_notes", content="设计备注：补充关卡节奏和体验设计思路。", sub_type="paragraph", placeholder="玩家体验目标、难度曲线、视觉主题", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_character_skill_table_components() -> list:
        template = PageTemplate(name="character_skill_table", display_name="角色技能表", icon="zap", category="media", description="角色能力与技能系统")
        template.add_component(TextBlockComponent(id="title", content="角色技能表", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="定义角色的技能、属性和成长系统。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TableComponent(
            id="skill_table",
            columns=[
                {"key": "skill_name", "title": "技能名称", "width": "20%"},
                {"key": "type", "title": "技能类型", "width": "15%"},
                {"key": "description", "title": "技能描述", "width": "30%"},
                {"key": "cooldown", "title": "冷却时间", "width": "10%"},
                {"key": "unlock", "title": "解锁条件", "width": "25%"},
            ],
            data=[
                {"skill_name": "火焰斩", "type": "主动", "description": "对前方敌人造成火属性伤害", "cooldown": "8s", "unlock": "等级5"},
                {"skill_name": "防御强化", "type": "被动", "description": "提升基础防御力", "cooldown": "-", "unlock": "等级3"},
            ],
            order=3,
        ))
        template.add_component(ListComponent(
            id="skill_upgrade",
            items=[
                {"label": "技能升级路线", "value": "upgrade", "description": "技能进阶路径和材料需求"},
                {"label": "技能组合推荐", "value": "combo", "description": "技能连招和协同效果"},
            ],
            list_type="definition",
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_narrative_branch_tree_components() -> list:
        template = PageTemplate(name="narrative_branch_tree", display_name="叙事分支树", icon="git-branch", category="media", description="剧情分支与对话树")
        template.add_component(TextBlockComponent(id="title", content="叙事分支树", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="设计故事剧情分支和对话选择树。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(FlowchartComponent(
            id="branch_flow",
            nodes=[
                {"id": "start", "label": "剧情起点", "type": "start_end"},
                {"id": "choice1", "label": "选择A：接受任务", "type": "decision"},
                {"id": "choice2", "label": "选择B：拒绝任务", "type": "decision"},
                {"id": "result1", "label": "支线剧情A", "type": "process"},
                {"id": "result2", "label": "支线剧情B", "type": "process"},
            ],
            edges=[
                {"from": "start", "to": "choice1", "label": "默认", "style": "solid"},
                {"from": "start", "to": "choice2", "label": "可选", "style": "dashed"},
                {"from": "choice1", "to": "result1", "label": "接受", "style": "solid"},
                {"from": "choice2", "to": "result2", "label": "拒绝", "style": "solid"},
            ],
            order=3,
        ))
        template.add_component(TextBlockComponent(id="branch_notes", content="分支条件说明：记录触发条件和后续影响。", sub_type="paragraph", placeholder="各分支的触发条件、角色关系影响、结局关联", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_scene_concept_set_components() -> list:
        template = PageTemplate(name="scene_concept_set", display_name="场景概念集", icon="image", category="media", description="场景概念设计图集")
        template.add_component(TextBlockComponent(id="title", content="场景概念集", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="收集和展示场景概念设计图。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(ImageGalleryComponent(
            id="concept_gallery",
            images=[
                {"url": "", "alt": "主场景全景", "caption": "主场景全景概念图", "width": 1920, "height": 1080},
                {"url": "", "alt": "室内细节", "caption": "室内环境细节设计", "width": 1920, "height": 1080},
                {"url": "", "alt": "夜景氛围", "caption": "夜晚场景氛围", "width": 1920, "height": 1080},
            ],
            layout="masonry",
            columns=3,
            order=3,
        ))
        template.add_component(TextBlockComponent(id="concept_notes", content="设计说明：记录场景风格和设计参考。", sub_type="paragraph", placeholder="色彩基调、光影参考、建筑风格说明", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_voice_script_table_components() -> list:
        template = PageTemplate(name="voice_script_table", display_name="配音脚本表", icon="mic", category="media", description="配音台词与录制管理")
        template.add_component(TextBlockComponent(id="title", content="配音脚本表", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="管理配音角色的台词脚本和录制进度。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TableComponent(
            id="script_table",
            columns=[
                {"key": "scene", "title": "场景", "width": "15%"},
                {"key": "character", "title": "角色", "width": "15%"},
                {"key": "line", "title": "台词内容", "width": "35%"},
                {"key": "emotion", "title": "情感指示", "width": "15%"},
                {"key": "status", "title": "录制状态", "width": "20%"},
            ],
            data=[
                {"scene": "第一幕", "character": "主角", "line": "示例台词文本", "emotion": "坚定", "status": "待录制"},
                {"scene": "第一幕", "character": "配角", "line": "回应台词", "emotion": "疑惑", "status": "已完成"},
            ],
            order=3,
        ))
        template.add_component(ListComponent(
            id="voice_director_notes",
            items=[
                {"label": "配音指导要点", "value": "direction", "description": "语速、语调、情感变化要求"},
                {"label": "已录制文件列表", "value": "recorded", "description": "已完成配音文件汇总"},
            ],
            list_type="definition",
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_game_mechanics_proto_components() -> list:
        template = PageTemplate(name="game_mechanics_proto", display_name="玩法原型文档", icon="controller", category="media", description="游戏核心玩法原型")
        template.add_component(TextBlockComponent(id="title", content="玩法原型文档", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="描述游戏核心玩法机制和交互原型。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(StepsComponent(
            id="mechanics_steps",
            steps=[
                {"id": "core_loop", "title": "核心循环", "description": "玩家操作-反馈循环", "status": "completed"},
                {"id": "interaction", "title": "交互方式", "description": "操作输入与响应", "status": "in_progress"},
                {"id": "feedback", "title": "反馈系统", "description": "视觉/听觉/触觉反馈", "status": "pending"},
                {"id": "balance", "title": "数值平衡", "description": "难度曲线与经济系统", "status": "pending"},
            ],
            current=1,
            order=3,
        ))
        template.add_component(TableComponent(
            id="mechanics_table",
            columns=[
                {"key": "mechanic", "title": "机制名称", "width": "20%"},
                {"key": "description", "title": "机制描述", "width": "40%"},
                {"key": "trigger", "title": "触发方式", "width": "20%"},
                {"key": "effect", "title": "效果", "width": "20%"},
            ],
            data=[
                {"mechanic": "跑酷移动", "description": "基础移动与跳跃", "trigger": "按键输入", "effect": "角色位移"},
                {"mechanic": "道具收集", "description": "场景道具拾取", "trigger": "碰撞检测", "effect": "获得物品"},
            ],
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    PAGE_TYPES = {
        "storyboard_panel": {
            "name": "storyboard_panel", "display_name": "分镜脚本板", "icon": "film",
            "category": "media", "description": "影视分镜头脚本设计",
            "default_schema": {"shots": [], "components": _create_storyboard_panel_components.__func__()}
        },
        "level_design_doc": {
            "name": "level_design_doc", "display_name": "关卡设计文档", "icon": "map",
            "category": "media", "description": "游戏关卡设计文档",
            "default_schema": {"level_data": {}, "components": _create_level_design_doc_components.__func__()}
        },
        "character_skill_table": {
            "name": "character_skill_table", "display_name": "角色技能表", "icon": "zap",
            "category": "media", "description": "角色能力与技能系统",
            "default_schema": {"skills": [], "components": _create_character_skill_table_components.__func__()}
        },
        "narrative_branch_tree": {
            "name": "narrative_branch_tree", "display_name": "叙事分支树", "icon": "git-branch",
            "category": "media", "description": "剧情分支与对话树",
            "default_schema": {"branches": [], "components": _create_narrative_branch_tree_components.__func__()}
        },
        "scene_concept_set": {
            "name": "scene_concept_set", "display_name": "场景概念集", "icon": "image",
            "category": "media", "description": "场景概念设计图集",
            "default_schema": {"concepts": [], "components": _create_scene_concept_set_components.__func__()}
        },
        "voice_script_table": {
            "name": "voice_script_table", "display_name": "配音脚本表", "icon": "mic",
            "category": "media", "description": "配音台词与录制管理",
            "default_schema": {"scripts": [], "components": _create_voice_script_table_components.__func__()}
        },
        "game_mechanics_proto": {
            "name": "game_mechanics_proto", "display_name": "玩法原型文档", "icon": "controller",
            "category": "media", "description": "游戏核心玩法原型",
            "default_schema": {"mechanics": [], "components": _create_game_mechanics_proto_components.__func__()}
        },
    }
