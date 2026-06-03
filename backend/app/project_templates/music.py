"""
音乐领域页面模板 - 结构图谱、编配表、歌词板、录音日志、音效卡片、采样库
"""
from app.page_components import (
    PageTemplate,
    TextBlockComponent, TableComponent, ListComponent, TimelineComponent,
    MindmapComponent, AudioPlayerComponent, FileRepoComponent,
    DividerComponent, SpacerComponent,
)


class MusicPages:
    """音乐领域页面模板"""

    @staticmethod
    def _create_structure_chart_components() -> list:
        template = PageTemplate(name="structure_chart", display_name="结构图谱", icon="git-branch", category="music", description="音乐整体结构图谱")
        template.add_component(TextBlockComponent(id="title", content="结构图谱", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="规划音乐作品的整体结构和段落编排。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(MindmapComponent(
            id="structure_map",
            nodes=[
                {"id": "root", "label": "乐曲结构", "parent_id": None, "color": "#1890FF"},
                {"id": "intro", "label": "前奏 Intro", "parent_id": "root", "color": "#52C41A"},
                {"id": "verse1", "label": "主歌 A段", "parent_id": "root", "color": "#13C2C2"},
                {"id": "chorus", "label": "副歌 Hook", "parent_id": "root", "color": "#FAAD14"},
                {"id": "bridge", "label": "桥段 Bridge", "parent_id": "root", "color": "#EB2F96"},
                {"id": "outro", "label": "尾奏 Outro", "parent_id": "root", "color": "#722ED1"},
                {"id": "verse2", "label": "主歌 B段", "parent_id": "root", "color": "#13C2C2"},
            ],
            layout="tree",
            order=3,
        ))
        template.add_component(TextBlockComponent(id="structure_notes", content="结构说明：记录段落长度、调性和情绪变化。", sub_type="paragraph", placeholder="各段落小节数、调式转换、速度变化、情绪走向", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_arrangement_table_components() -> list:
        template = PageTemplate(name="arrangement_table", display_name="编配表", icon="music", category="music", description="乐器编配与声部分配")
        template.add_component(TextBlockComponent(id="title", content="编配表", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="设计各乐器的声部编配和音色安排。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TableComponent(
            id="arrangement_grid",
            columns=[
                {"key": "section", "title": "段落", "width": "12%"},
                {"key": "piano", "title": "钢琴", "width": "18%"},
                {"key": "strings", "title": "弦乐", "width": "18%"},
                {"key": "drums", "title": "鼓组", "width": "18%"},
                {"key": "bass", "title": "贝斯", "width": "18%"},
                {"key": "vocal", "title": "人声", "width": "16%"},
            ],
            data=[
                {"section": "前奏", "piano": "分解和弦", "strings": "长音铺底", "drums": "无", "bass": "无", "vocal": "无"},
                {"section": "主歌A", "piano": "和弦伴奏", "strings": "拨奏", "drums": "轻拍镲", "bass": "根音", "vocal": "主旋律"},
                {"section": "副歌", "piano": "柱式和弦", "strings": "齐奏", "drums": "强拍鼓", "bass": "律动线", "vocal": "高八度"},
            ],
            order=3,
        ))
        template.add_component(ListComponent(
            id="instrument_notes",
            items=[
                {"label": "音色选择", "value": "timbre", "description": "各乐器音色库和预设"},
                {"label": "效果链", "value": "fx", "description": "混响、延迟等效果器设置"},
            ],
            list_type="definition",
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_lyrics_board_components() -> list:
        template = PageTemplate(name="lyrics_board", display_name="歌词板", icon="edit-3", category="music", description="歌词创作与编辑")
        template.add_component(TextBlockComponent(id="title", content="歌词板", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="创作和编辑歌词文本。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TextBlockComponent(id="lyrics_section1", content="[主歌]\n第一段歌词内容\n第二行歌词内容\n\n[副歌]\n副歌歌词内容\n重复副歌歌词", sub_type="quote", placeholder="在此填写歌词段落", order=3))
        template.add_component(TextBlockComponent(id="lyrics_notes", content="创作备注：记录押韵方案、主题意象和修改想法。", sub_type="paragraph", placeholder="歌词主题、押韵结构、修辞手法、修改历史", order=4))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_recording_log_components() -> list:
        template = PageTemplate(name="recording_log", display_name="录音日志", icon="mic", category="music", description="录音过程与版本记录")
        template.add_component(TextBlockComponent(id="title", content="录音日志", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="记录录音过程和版本迭代信息。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(TimelineComponent(
            id="recording_timeline",
            events=[
                {"id": "take1", "title": "第一次录音", "description": "原始素材录制，麦克风位置A", "date": "2026-05-01", "icon": "circle", "color": "#1890FF"},
                {"id": "take2", "title": "第二次录音", "description": "调整话放增益后重录", "date": "2026-05-02", "icon": "circle", "color": "#52C41A"},
                {"id": "overdub", "title": "叠加录音", "description": "叠加和声和副旋律", "date": "2026-05-03", "icon": "circle", "color": "#FAAD14"},
                {"id": "comp", "title": "合成选段", "description": "选择最佳片段组合", "date": "2026-05-04", "icon": "circle", "color": "#722ED1"},
            ],
            layout="vertical",
            order=3,
        ))
        template.add_component(TableComponent(
            id="track_list",
            columns=[
                {"key": "track", "title": "音轨", "width": "20%"},
                {"key": "take", "title": "录音次数", "width": "15%"},
                {"key": "best_take", "title": "最佳选段", "width": "25%"},
                {"key": "notes", "title": "备注", "width": "40%"},
            ],
            data=[
                {"track": "人声主轨", "take": "3次", "best_take": "第2次", "notes": "感情饱满，音准佳"},
                {"track": "木吉他", "take": "2次", "best_take": "第1次", "notes": "音色自然"},
            ],
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_sound_design_card_components() -> list:
        template = PageTemplate(name="sound_design_card", display_name="音效设计卡", icon="volume-2", category="music", description="音效设计与参数记录")
        template.add_component(TextBlockComponent(id="title", content="音效设计卡", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="设计音效的参数配置和试听管理。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(AudioPlayerComponent(
            id="sound_preview",
            url="",
            artist="音效设计师",
            order=3,
        ))
        template.add_component(ListComponent(
            id="sound_params",
            items=[
                {"label": "音效类型", "value": "ambient", "description": "环境音效/Foley/合成音"},
                {"label": "音色特征", "value": "timbre", "description": "温暖/明亮/低沉/空旷"},
                {"label": "处理链", "value": "chain", "description": "EQ -> Compression -> Reverb"},
                {"label": "时长", "value": "duration", "description": "3.5秒"},
                {"label": "文件格式", "value": "format", "description": "WAV 48kHz 24bit"},
            ],
            list_type="property",
            order=4,
        ))
        template.add_component(TextBlockComponent(id="design_notes", content="设计说明：记录创意来源和音效上下文。", sub_type="paragraph", placeholder="应用场景、参考素材、设计思路、修改记录", order=5))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    @staticmethod
    def _create_sample_library_components() -> list:
        template = PageTemplate(name="sample_library", display_name="采样库", icon="folder", category="music", description="音频采样素材管理")
        template.add_component(TextBlockComponent(id="title", content="采样库", sub_type="heading", level=1, order=0))
        template.add_component(TextBlockComponent(id="desc", content="管理和分类音频采样素材。", sub_type="paragraph", order=1))
        template.add_component(DividerComponent(order=2))
        template.add_component(FileRepoComponent(
            id="sample_files",
            files=[],
            allow_upload=True,
            order=3,
        ))
        template.add_component(TableComponent(
            id="sample_catalog",
            columns=[
                {"key": "name", "title": "采样名称", "width": "20%"},
                {"key": "category", "title": "分类", "width": "15%"},
                {"key": "key", "title": "调性", "width": "10%"},
                {"key": "bpm", "title": "速度", "width": "10%"},
                {"key": "source", "title": "来源", "width": "20%"},
                {"key": "tags", "title": "标签", "width": "25%"},
            ],
            data=[
                {"name": "Ambient Pad 01", "category": "氛围", "key": "C大调", "bpm": "80", "source": "合成器", "tags": "环境,铺垫"},
                {"name": "Drum Loop 05", "category": "鼓组", "key": "-", "bpm": "120", "source": "采样包", "tags": "节奏,律动"},
                {"name": "Bass Line 03", "category": "贝斯", "key": "D小调", "bpm": "100", "source": "录音", "tags": "低音,律动"},
            ],
            order=4,
        ))
        template.add_component(SpacerComponent(height=24, order=99))
        return template.get_default_schema()["components"]

    PAGE_TYPES = {
        "structure_chart": {
            "name": "structure_chart", "display_name": "结构图谱", "icon": "git-branch",
            "category": "music", "description": "音乐整体结构图谱",
            "default_schema": {"sections": [], "components": _create_structure_chart_components.__func__()}
        },
        "arrangement_table": {
            "name": "arrangement_table", "display_name": "编配表", "icon": "music",
            "category": "music", "description": "乐器编配与声部分配",
            "default_schema": {"arrangement": [], "components": _create_arrangement_table_components.__func__()}
        },
        "lyrics_board": {
            "name": "lyrics_board", "display_name": "歌词板", "icon": "edit-3",
            "category": "music", "description": "歌词创作与编辑",
            "default_schema": {"lyrics": "", "components": _create_lyrics_board_components.__func__()}
        },
        "recording_log": {
            "name": "recording_log", "display_name": "录音日志", "icon": "mic",
            "category": "music", "description": "录音过程与版本记录",
            "default_schema": {"takes": [], "components": _create_recording_log_components.__func__()}
        },
        "sound_design_card": {
            "name": "sound_design_card", "display_name": "音效设计卡", "icon": "volume-2",
            "category": "music", "description": "音效设计与参数记录",
            "default_schema": {"sound": {}, "components": _create_sound_design_card_components.__func__()}
        },
        "sample_library": {
            "name": "sample_library", "display_name": "采样库", "icon": "folder",
            "category": "music", "description": "音频采样素材管理",
            "default_schema": {"samples": [], "components": _create_sample_library_components.__func__()}
        },
    }
