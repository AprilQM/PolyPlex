"""
编程领域页面模板 - 20个软件开发生命周期页面类型
"""
from app.page_components import (
    PageTemplate,
    TextBlockComponent, ImageGalleryComponent, VideoEmbedComponent,
    FileRepoComponent, AttachmentListComponent,
    TableComponent, KanbanComponent, TimelineComponent,
    StepsComponent, ListComponent,
    MindmapComponent, FlowchartComponent, RelationGraphComponent,
    DataChartComponent,
    MetricCardComponent, ProgressBarComponent, CounterComponent,
    ScorecardComponent, FormulaComponent,
    CommentAnchorComponent, VoteModuleComponent, TaskAssignComponent,
    ChangelogComponent,
    PageRefComponent, EmbedViewComponent, BreadcrumbComponent,
    TagSetComponent,
    BizCanvasComponent, PersonaCardComponent, SwotComponent,
    CompeteMatrixComponent,
    DividerComponent, SpacerComponent, MultiColumnComponent,
    TabsComponent, AnchorTocComponent,
)


class CodePages:
    """编程领域页面模板 - 覆盖软件开发生命周期"""

    # ============================================================
    # 1. system_arch - 系统架构
    # ============================================================
    @staticmethod
    def _create_system_arch_components() -> list:
        template = PageTemplate(
            name="system_arch",
            display_name="系统架构",
            icon="architecture",
            category="code",
            description="系统整体架构设计与服务关系图",
        )
        template.add_component(TextBlockComponent(
            id="system_arch_title", content="系统架构", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="system_arch_desc",
            content="描述系统整体架构设计、服务划分、模块依赖关系与通信方式。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(FlowchartComponent(
            id="system_arch_flow",
            title="系统架构图",
            nodes=[
                {"id": "gateway", "label": "API Gateway", "type": "process"},
                {"id": "auth", "label": "Auth Service", "type": "process"},
                {"id": "user", "label": "User Service", "type": "process"},
                {"id": "data", "label": "Data Service", "type": "process"},
                {"id": "cache", "label": "Redis Cache", "type": "input_output"},
                {"id": "db", "label": "Database", "type": "input_output"},
            ],
            edges=[
                {"from": "gateway", "to": "auth", "label": "authenticate", "style": "solid"},
                {"from": "gateway", "to": "user", "label": "route", "style": "solid"},
                {"from": "gateway", "to": "data", "label": "route", "style": "solid"},
                {"from": "user", "to": "db", "label": "persist", "style": "dashed"},
                {"from": "data", "to": "cache", "label": "cache", "style": "dotted"},
                {"from": "data", "to": "db", "label": "persist", "style": "dashed"},
            ],
            order=3,
        ))

        template.add_component(RelationGraphComponent(
            id="system_arch_relations",
            title="服务依赖关系",
            nodes=[
                {"id": "api", "label": "API Layer", "group": "gateway"},
                {"id": "svc", "label": "Service Layer", "group": "service"},
                {"id": "dal", "label": "Data Layer", "group": "data"},
                {"id": "cache_node", "label": "Cache", "group": "infra"},
                {"id": "mq", "label": "Message Queue", "group": "infra"},
            ],
            edges=[
                {"from": "api", "to": "svc", "label": "depends", "direction": "one_way"},
                {"from": "svc", "to": "dal", "label": "depends", "direction": "one_way"},
                {"from": "svc", "to": "cache_node", "label": "reads", "direction": "two_way"},
                {"from": "svc", "to": "mq", "label": "publishes", "direction": "one_way"},
            ],
            order=4,
        ))

        template.add_component(TableComponent(
            id="system_arch_services",
            title="服务说明表",
            columns=[
                {"key": "service", "title": "服务名", "width": "20%"},
                {"key": "responsibility", "title": "职责", "width": "35%"},
                {"key": "tech", "title": "技术栈", "width": "20%"},
                {"key": "replicas", "title": "实例数", "width": "10%"},
            ],
            data=[
                {"service": "API Gateway", "responsibility": "请求路由与限流", "tech": "Nginx/Kong", "replicas": "2"},
                {"service": "Auth Service", "responsibility": "身份认证与授权", "tech": "FastAPI + JWT", "replicas": "2"},
                {"service": "User Service", "responsibility": "用户管理与资料存储", "tech": "FastAPI + MySQL", "replicas": "3"},
            ],
            order=5,
        ))

        template.add_component(TagSetComponent(
            id="system_arch_tags",
            tags=[
                {"name": "微服务", "color": "#1890FF", "count": 5},
                {"name": "RESTful", "color": "#52C41A", "count": 3},
                {"name": "Docker", "color": "#FAAD14", "count": 4},
            ],
            allow_create=True,
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 2. api_definition - API定义
    # ============================================================
    @staticmethod
    def _create_api_definition_components() -> list:
        template = PageTemplate(
            name="api_definition",
            display_name="API 定义",
            icon="api",
            category="code",
            description="API 接口定义与文档",
        )
        template.add_component(TextBlockComponent(
            id="api_def_title", content="API 定义", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="api_def_desc",
            content="项目所有 API 接口的详细定义，包括请求方法、路径、参数和响应格式。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="api_endpoints",
            title="接口列表",
            columns=[
                {"key": "method", "title": "方法", "width": "10%"},
                {"key": "path", "title": "路径", "width": "30%"},
                {"key": "description", "title": "描述", "width": "30%"},
                {"key": "auth", "title": "认证", "width": "10%"},
                {"key": "status", "title": "状态", "width": "10%"},
            ],
            data=[
                {"method": "GET", "path": "/api/v1/users", "description": "获取用户列表", "auth": "JWT", "status": "稳定"},
                {"method": "POST", "path": "/api/v1/users", "description": "创建用户", "auth": "JWT", "status": "稳定"},
                {"method": "GET", "path": "/api/v1/users/{id}", "description": "获取用户详情", "auth": "JWT", "status": "稳定"},
                {"method": "PUT", "path": "/api/v1/users/{id}", "description": "更新用户信息", "auth": "JWT", "status": "进行中"},
            ],
            order=3,
        ))

        template.add_component(TextBlockComponent(
            id="api_request_example",
            content='''# 获取用户列表请求示例
curl -X GET "https://api.example.com/api/v1/users?page=1&limit=20" \\
  -H "Authorization: Bearer <token>" \\
  -H "Content-Type: application/json"

# 响应示例
{
  "code": 200,
  "data": {
    "users": [
      {"id": 1, "name": "Alice", "email": "alice@example.com"}
    ],
    "total": 100,
    "page": 1
  },
  "message": "success"
}''',
            sub_type="code_block", language="bash", title="请求/响应示例", order=4,
        ))

        template.add_component(TabsComponent(
            id="api_modules",
            title="API 模块导航",
            tabs=[
                {"key": "user", "label": "用户模块", "icon": "user", "content": []},
                {"key": "order", "label": "订单模块", "icon": "order", "content": []},
                {"key": "payment", "label": "支付模块", "icon": "payment", "content": []},
            ],
            order=5,
        ))

        template.add_component(TagSetComponent(
            id="api_tags",
            tags=[
                {"name": "RESTful", "color": "#1890FF", "count": 12},
                {"name": "GraphQL", "color": "#EB2F96", "count": 2},
                {"name": "WebSocket", "color": "#52C41A", "count": 1},
            ],
            allow_create=True,
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 3. data_model - 数据模型
    # ============================================================
    @staticmethod
    def _create_data_model_components() -> list:
        template = PageTemplate(
            name="data_model",
            display_name="数据模型",
            icon="database",
            category="code",
            description="数据库表结构设计与实体关系",
        )
        template.add_component(TextBlockComponent(
            id="data_model_title", content="数据模型", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="data_model_desc",
            content="数据库表结构、字段定义、索引和实体关系设计文档。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(RelationGraphComponent(
            id="data_model_er",
            title="实体关系图 (ER)",
            nodes=[
                {"id": "user", "label": "User", "group": "entity"},
                {"id": "order", "label": "Order", "group": "entity"},
                {"id": "product", "label": "Product", "group": "entity"},
                {"id": "category", "label": "Category", "group": "entity"},
            ],
            edges=[
                {"from": "user", "to": "order", "label": "has many", "direction": "one_way"},
                {"from": "order", "to": "product", "label": "belongs to", "direction": "one_way"},
                {"from": "product", "to": "category", "label": "belongs to", "direction": "one_way"},
            ],
            order=3,
        ))

        template.add_component(TableComponent(
            id="data_model_tables",
            title="表结构定义",
            columns=[
                {"key": "table", "title": "表名", "width": "15%"},
                {"key": "field", "title": "字段", "width": "20%"},
                {"key": "type", "title": "类型", "width": "15%"},
                {"key": "constraint", "title": "约束", "width": "20%"},
                {"key": "description", "title": "说明", "width": "30%"},
            ],
            data=[
                {"table": "users", "field": "id", "type": "BIGINT", "constraint": "PK AUTO_INC", "description": "用户ID"},
                {"table": "users", "field": "email", "type": "VARCHAR(255)", "constraint": "UNIQUE NOT NULL", "description": "邮箱"},
                {"table": "users", "field": "password_hash", "type": "VARCHAR(128)", "constraint": "NOT NULL", "description": "密码哈希"},
                {"table": "orders", "field": "id", "type": "BIGINT", "constraint": "PK AUTO_INC", "description": "订单ID"},
                {"table": "orders", "field": "user_id", "type": "BIGINT", "constraint": "FK -> users.id", "description": "用户ID"},
            ],
            order=4,
        ))

        template.add_component(ListComponent(
            id="data_model_indexes",
            title="索引说明",
            items=[
                {"label": "users.email", "value": "唯一索引", "description": "加速邮箱登录查询", "icon": "index"},
                {"label": "orders.user_id", "value": "普通索引", "description": "加速用户订单查询", "icon": "index"},
                {"label": "orders.created_at", "value": "普通索引", "description": "加速时间范围查询", "icon": "index"},
            ],
            list_type="property",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 4. tech_selection - 技术选型
    # ============================================================
    @staticmethod
    def _create_tech_selection_components() -> list:
        template = PageTemplate(
            name="tech_selection",
            display_name="技术选型",
            icon="selection",
            category="code",
            description="技术方案选型与对比分析",
        )
        template.add_component(TextBlockComponent(
            id="tech_selection_title", content="技术选型", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="tech_selection_desc",
            content="项目中使用的技术栈、框架、工具及其选型理由和对比分析。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="tech_compare",
            title="技术方案对比",
            columns=[
                {"key": "category", "title": "类别", "width": "15%"},
                {"key": "chosen", "title": "选型方案", "width": "25%"},
                {"key": "alternative", "title": "备选方案", "width": "25%"},
                {"key": "reason", "title": "选择理由", "width": "35%"},
            ],
            data=[
                {"category": "后端框架", "chosen": "FastAPI", "alternative": "Django/Flask", "reason": "异步支持好、自动生成OpenAPI文档"},
                {"category": "数据库", "chosen": "PostgreSQL", "alternative": "MySQL", "reason": "JSON支持好、扩展性强"},
                {"category": "缓存", "chosen": "Redis", "alternative": "Memcached", "reason": "数据结构丰富、支持持久化"},
                {"category": "前端", "chosen": "React + TypeScript", "alternative": "Vue", "reason": "生态成熟、团队经验丰富"},
            ],
            order=3,
        ))

        template.add_component(ScorecardComponent(
            id="tech_evaluation",
            title="技术综合评分",
            dimensions=[
                {"name": "开发效率", "weight": 0.3, "max_score": 10, "score": 9},
                {"name": "性能表现", "weight": 0.25, "max_score": 10, "score": 8},
                {"name": "可维护性", "weight": 0.2, "max_score": 10, "score": 8},
                {"name": "社区生态", "weight": 0.15, "max_score": 10, "score": 9},
                {"name": "学习成本", "weight": 0.1, "max_score": 10, "score": 7},
            ],
            score_type="numeric",
            order=4,
        ))

        template.add_component(ListComponent(
            id="tech_pros_cons",
            title="选型优劣分析",
            items=[
                {"label": "FastAPI", "value": "优势", "description": "高性能异步框架，自动生成API文档", "icon": "check", "checked": True},
                {"label": "FastAPI", "value": "劣势", "description": "社区相对Django较小", "icon": "close", "checked": False},
                {"label": "PostgreSQL", "value": "优势", "description": "ACID事务，支持JSON和GIS", "icon": "check", "checked": True},
                {"label": "PostgreSQL", "value": "劣势", "description": "写密集型场景不如MySQL", "icon": "close", "checked": False},
            ],
            list_type="property",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 5. user_story_map - 用户故事地图
    # ============================================================
    @staticmethod
    def _create_user_story_map_components() -> list:
        template = PageTemplate(
            name="user_story_map",
            display_name="用户故事地图",
            icon="story_map",
            category="code",
            description="用户故事地图与需求优先级规划",
        )
        template.add_component(TextBlockComponent(
            id="story_map_title", content="用户故事地图", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="story_map_desc",
            content="按用户旅程组织的用户故事地图，展示功能需求与发布规划。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(KanbanComponent(
            id="story_map_board",
            title="故事地图看板",
            columns=[
                {"id": "backlog", "title": "需求待办", "color": "#D9D9D9"},
                {"id": "current", "title": "当前迭代", "color": "#1890FF"},
                {"id": "in_progress", "title": "开发中", "color": "#FAAD14"},
                {"id": "done", "title": "已完成", "color": "#52C41A"},
            ],
            cards=[
                {"id": "s1", "title": "用户注册", "description": "作为用户，我需要注册账号", "column_id": "done", "priority": "high", "assignee": "Alice"},
                {"id": "s2", "title": "用户登录", "description": "作为用户，我需要登录系统", "column_id": "current", "priority": "high", "assignee": "Bob"},
                {"id": "s3", "title": "密码重置", "description": "作为用户，我需要重置密码", "column_id": "backlog", "priority": "medium", "assignee": ""},
                {"id": "s4", "title": "个人资料编辑", "description": "作为用户，我需要编辑个人资料", "column_id": "in_progress", "priority": "medium", "assignee": "Alice"},
            ],
            order=3,
        ))

        template.add_component(ListComponent(
            id="story_details",
            title="故事详情清单",
            items=[
                {"label": "US-001", "value": "用户注册", "description": "邮箱+密码注册，邮箱验证", "icon": "story"},
                {"label": "US-002", "value": "用户登录", "description": "支持邮箱/手机号登录", "icon": "story"},
                {"label": "US-003", "value": "密码重置", "description": "通过邮箱验证码重置密码", "icon": "story"},
                {"label": "US-004", "value": "个人资料", "description": "编辑头像、昵称、个人简介", "icon": "story"},
            ],
            list_type="property",
            order=4,
        ))

        template.add_component(TimelineComponent(
            id="story_releases",
            title="发布规划时间线",
            events=[
                {"id": "r1", "title": "MVP v1.0", "description": "核心认证功能", "date": "2026-01", "color": "#1890FF"},
                {"id": "r2", "title": "v1.1", "description": "个人中心与配置", "date": "2026-02", "color": "#52C41A"},
                {"id": "r3", "title": "v2.0", "description": "社交与互动功能", "date": "2026-Q2", "color": "#FAAD14"},
            ],
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 6. test_case_set - 测试用例集
    # ============================================================
    @staticmethod
    def _create_test_case_set_components() -> list:
        template = PageTemplate(
            name="test_case_set",
            display_name="测试用例集",
            icon="test_case",
            category="code",
            description="单元测试与集成测试用例管理",
        )
        template.add_component(TextBlockComponent(
            id="test_case_title", content="测试用例集", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="test_case_desc",
            content="项目测试用例列表，覆盖单元测试、集成测试和端到端测试。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="test_case_list",
            title="测试用例列表",
            columns=[
                {"key": "id", "title": "编号", "width": "10%"},
                {"key": "module", "title": "模块", "width": "15%"},
                {"key": "description", "title": "测试描述", "width": "30%"},
                {"key": "type", "title": "类型", "width": "12%"},
                {"key": "status", "title": "状态", "width": "10%"},
                {"key": "owner", "title": "责任人", "width": "10%"},
            ],
            data=[
                {"id": "TC-001", "module": "Auth", "description": "验证用户注册成功", "type": "单元测试", "status": "通过", "owner": "Alice"},
                {"id": "TC-002", "module": "Auth", "description": "验证登录失败处理", "type": "单元测试", "status": "通过", "owner": "Alice"},
                {"id": "TC-003", "module": "User", "description": "验证用户资料更新API", "type": "集成测试", "status": "进行中", "owner": "Bob"},
                {"id": "TC-004", "module": "Order", "description": "验证下单全流程", "type": "E2E", "status": "待执行", "owner": "Bob"},
            ],
            order=3,
        ))

        template.add_component(ProgressBarComponent(
            id="test_coverage",
            title="测试覆盖率",
            percentage=72.5,
            style="bar",
            color="#1890FF",
            show_label=True,
            order=4,
        ))

        template.add_component(StepsComponent(
            id="test_steps",
            title="测试执行步骤",
            steps=[
                {"id": "s1", "title": "编写用例", "description": "编写测试用例文档", "status": "completed"},
                {"id": "s2", "title": "单元测试", "description": "执行单元测试", "status": "completed"},
                {"id": "s3", "title": "集成测试", "description": "执行集成测试", "status": "in_progress"},
                {"id": "s4", "title": "E2E测试", "description": "执行端到端测试", "status": "pending"},
            ],
            current=2,
            order=5,
        ))

        template.add_component(MetricCardComponent(
            id="test_metrics",
            title="测试指标",
            value="85",
            label="总用例数",
            suffix="个",
            size="small",
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 7. deploy_flow - 部署流程
    # ============================================================
    @staticmethod
    def _create_deploy_flow_components() -> list:
        template = PageTemplate(
            name="deploy_flow",
            display_name="部署流程",
            icon="deploy",
            category="code",
            description="CI/CD 部署流水线与环境管理",
        )
        template.add_component(TextBlockComponent(
            id="deploy_title", content="部署流程", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="deploy_desc",
            content="持续集成与持续部署流水线，包括环境配置、部署步骤和回滚策略。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(FlowchartComponent(
            id="deploy_pipeline",
            title="CI/CD 流水线",
            nodes=[
                {"id": "code", "label": "Code Commit", "type": "start_end"},
                {"id": "build", "label": "Build & Test", "type": "process"},
                {"id": "docker", "label": "Docker Build", "type": "process"},
                {"id": "staging", "label": "Deploy Staging", "type": "process"},
                {"id": "test", "label": "Integration Test", "type": "decision"},
                {"id": "prod", "label": "Deploy Production", "type": "process"},
            ],
            edges=[
                {"from": "code", "to": "build", "label": "trigger", "style": "solid"},
                {"from": "build", "to": "docker", "label": "on pass", "style": "solid"},
                {"from": "docker", "to": "staging", "label": "push", "style": "solid"},
                {"from": "staging", "to": "test", "label": "run", "style": "solid"},
                {"from": "test", "to": "prod", "label": "pass", "style": "solid"},
                {"from": "test", "to": "staging", "label": "fail", "style": "dashed"},
            ],
            order=3,
        ))

        template.add_component(StepsComponent(
            id="deploy_steps",
            title="部署步骤说明",
            steps=[
                {"id": "d1", "title": "代码提交", "description": "推送到 main 分支", "status": "completed"},
                {"id": "d2", "title": "自动构建", "description": "GitHub Actions 构建", "status": "completed"},
                {"id": "d3", "title": "镜像打包", "description": "Docker 镜像构建与推送", "status": "completed"},
                {"id": "d4", "title": "预发布部署", "description": "部署到 Staging 环境", "status": "in_progress"},
                {"id": "d5", "title": "生产部署", "description": "灰度发布到线上", "status": "pending"},
            ],
            current=3,
            order=4,
        ))

        template.add_component(ListComponent(
            id="deploy_environments",
            title="环境配置",
            items=[
                {"label": "开发环境", "value": "dev", "description": "本地开发调试", "icon": "env"},
                {"label": "测试环境", "value": "staging", "description": "集成测试验证", "icon": "env"},
                {"label": "预发布环境", "value": "pre-prod", "description": "上线前验收", "icon": "env"},
                {"label": "生产环境", "value": "prod", "description": "线上正式服务", "icon": "env"},
            ],
            list_type="property",
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 8. tech_debt - 技术债务
    # ============================================================
    @staticmethod
    def _create_tech_debt_components() -> list:
        template = PageTemplate(
            name="tech_debt",
            display_name="技术债务",
            icon="tech_debt",
            category="code",
            description="技术债务追踪与管理",
        )
        template.add_component(TextBlockComponent(
            id="tech_debt_title", content="技术债务", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="tech_debt_desc",
            content="记录和追踪项目中的技术债务项，包括遗留问题、待重构模块和需要优化的设计。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="tech_debt_items",
            title="债务清单",
            columns=[
                {"key": "id", "title": "编号", "width": "8%"},
                {"key": "description", "title": "描述", "width": "30%"},
                {"key": "impact", "title": "影响范围", "width": "20%"},
                {"key": "priority", "title": "优先级", "width": "10%"},
                {"key": "effort", "title": "预估工时", "width": "10%"},
                {"key": "owner", "title": "负责人", "width": "10%"},
            ],
            data=[
                {"id": "TD-001", "description": "旧版ORM查询未使用连接池", "impact": "数据库性能", "priority": "高", "effort": "2d", "owner": "Alice"},
                {"id": "TD-002", "description": "前端组件缺少TypeScript类型定义", "impact": "开发效率", "priority": "中", "effort": "3d", "owner": "Bob"},
                {"id": "TD-003", "description": "日志收集缺少链路追踪ID", "impact": "排查问题", "priority": "高", "effort": "1d", "owner": "Charlie"},
                {"id": "TD-004", "description": "单元测试覆盖率不足30%", "impact": "代码质量", "priority": "低", "effort": "5d", "owner": ""},
            ],
            order=3,
        ))

        template.add_component(MetricCardComponent(
            id="debt_metric_total",
            value="4",
            label="待处理债务",
            prefix="",
            suffix="项",
            trend="up",
            size="medium",
            order=4,
        ))

        template.add_component(ProgressBarComponent(
            id="debt_resolution",
            title="债务解决进度",
            percentage=35.0,
            style="bar",
            color="#FAAD14",
            show_label=True,
            order=5,
        ))

        template.add_component(TaskAssignComponent(
            id="debt_task",
            title="当前治理任务",
            assignee="Alice",
            status="in_progress",
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 9. code_review_list - 代码审查清单
    # ============================================================
    @staticmethod
    def _create_code_review_list_components() -> list:
        template = PageTemplate(
            name="code_review_list",
            display_name="代码审查清单",
            icon="code_review",
            category="code",
            description="代码审查清单与评审追踪",
        )
        template.add_component(TextBlockComponent(
            id="review_title", content="代码审查清单", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="review_desc",
            content="代码评审任务列表，确保代码质量和规范符合项目标准。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="review_items",
            title="审查任务列表",
            columns=[
                {"key": "pr_id", "title": "PR编号", "width": "10%"},
                {"key": "title", "title": "标题", "width": "25%"},
                {"key": "author", "title": "作者", "width": "10%"},
                {"key": "reviewer", "title": "审查人", "width": "10%"},
                {"key": "status", "title": "状态", "width": "10%"},
                {"key": "comments", "title": "评论数", "width": "8%"},
            ],
            data=[
                {"pr_id": "#42", "title": "feat: 添加用户导出功能", "author": "Alice", "reviewer": "Bob", "status": "审查中", "comments": "3"},
                {"pr_id": "#41", "title": "fix: 修复登录超时问题", "author": "Bob", "reviewer": "Charlie", "status": "待审查", "comments": "0"},
                {"pr_id": "#40", "title": "refactor: 重构缓存层", "author": "Charlie", "reviewer": "Alice", "status": "已通过", "comments": "5"},
            ],
            order=3,
        ))

        template.add_component(ListComponent(
            id="review_checklist",
            title="审查清单",
            items=[
                {"label": "代码风格", "value": "符合ESLint/PEP8规范", "description": "检查格式化问题", "icon": "checklist", "checked": True},
                {"label": "单元测试", "value": "新增代码有对应测试", "description": "覆盖率不低于80%", "icon": "checklist", "checked": True},
                {"label": "安全性", "value": "无SQL注入/XSS风险", "description": "检查输入验证", "icon": "checklist", "checked": False},
                {"label": "性能", "value": "无N+1查询等问题", "description": "检查数据库查询", "icon": "checklist", "checked": False},
            ],
            list_type="definition",
            show_checkbox=True,
            order=4,
        ))

        template.add_component(MetricCardComponent(
            id="review_metrics",
            title="审查统计",
            value="12",
            label="本周审查数",
            prefix="共",
            suffix="个PR",
            trend="up",
            size="small",
            order=5,
        ))

        template.add_component(TaskAssignComponent(
            id="review_assign",
            title="指定审查人",
            assignee="Bob",
            status="pending",
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 10. code_snippet_lib - 代码片段库
    # ============================================================
    @staticmethod
    def _create_code_snippet_lib_components() -> list:
        template = PageTemplate(
            name="code_snippet_lib",
            display_name="代码片段库",
            icon="snippet",
            category="code",
            description="常用代码片段与工具函数库",
        )
        template.add_component(TextBlockComponent(
            id="snippet_title", content="代码片段库", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="snippet_desc",
            content="项目中常用的代码片段、工具函数和最佳实践示例。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(TextBlockComponent(
            id="snippet_1",
            content='''from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """验证JWT令牌并返回当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    user = await get_user_by_id(payload.get("sub"))
    if user is None:
        raise credentials_exception
    return user''',
            sub_type="code_block", language="python", title="JWT认证中间件", order=3,
        ))

        template.add_component(TextBlockComponent(
            id="snippet_2",
            content='''from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+asyncmy://user:pass@localhost:3306/db"
engine = create_async_engine(DATABASE_URL, echo=True, pool_size=10)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()''',
            sub_type="code_block", language="python", title="异步数据库连接", order=4,
        ))

        template.add_component(TagSetComponent(
            id="snippet_tags",
            tags=[
                {"name": "Python", "color": "#1890FF", "count": 8},
                {"name": "JavaScript", "color": "#FAAD14", "count": 5},
                {"name": "SQL", "color": "#52C41A", "count": 3},
                {"name": "Docker", "color": "#EB2F96", "count": 2},
            ],
            allow_create=True,
            order=5,
        ))

        template.add_component(TableComponent(
            id="snippet_index",
            title="片段索引",
            columns=[
                {"key": "name", "title": "名称", "width": "25%"},
                {"key": "language", "title": "语言", "width": "15%"},
                {"key": "description", "title": "用途", "width": "40%"},
                {"key": "usage", "title": "使用频率", "width": "15%"},
            ],
            data=[
                {"name": "JWT认证中间件", "language": "Python", "description": "FastAPI JWT令牌验证", "usage": "高频"},
                {"name": "异步数据库连接", "language": "Python", "description": "SQLAlchemy异步引擎配置", "usage": "高频"},
                {"name": "API响应封装", "language": "Python", "description": "统一响应格式", "usage": "高频"},
                {"name": "分页查询工具", "language": "Python", "description": "通用分页查询函数", "usage": "中频"},
            ],
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 11. bug_tracker - Bug追踪
    # ============================================================
    @staticmethod
    def _create_bug_tracker_components() -> list:
        template = PageTemplate(
            name="bug_tracker",
            display_name="Bug 追踪",
            icon="bug",
            category="code",
            description="Bug 缺陷追踪与修复管理",
        )
        template.add_component(TextBlockComponent(
            id="bug_title", content="Bug 追踪", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="bug_desc",
            content="缺陷报告、优先级排序与修复进度跟踪。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(KanbanComponent(
            id="bug_kanban",
            title="Bug 看板",
            columns=[
                {"id": "new", "title": "新提交", "color": "#FAAD14"},
                {"id": "triaged", "title": "已确认", "color": "#1890FF"},
                {"id": "fixing", "title": "修复中", "color": "#722ED1"},
                {"id": "testing", "title": "测试中", "color": "#13C2C2"},
                {"id": "closed", "title": "已关闭", "color": "#52C41A"},
            ],
            cards=[
                {"id": "b1", "title": "登录页面502错误", "description": "高并发时网关超时", "column_id": "fixing", "priority": "urgent", "assignee": "Alice"},
                {"id": "b2", "title": "用户头像上传失败", "description": "文件大小限制未生效", "column_id": "new", "priority": "high", "assignee": ""},
                {"id": "b3", "title": "搜索分页偏移错误", "description": "第3页后数据重复", "column_id": "triaged", "priority": "medium", "assignee": "Bob"},
                {"id": "b4", "title": "邮件模板渲染异常", "description": "特殊字符导致模板解析失败", "column_id": "closed", "priority": "low", "assignee": "Charlie"},
            ],
            order=3,
        ))

        template.add_component(TableComponent(
            id="bug_list",
            title="Bug 详情列表",
            columns=[
                {"key": "id", "title": "编号", "width": "8%"},
                {"key": "title", "title": "标题", "width": "20%"},
                {"key": "severity", "title": "严重程度", "width": "10%"},
                {"key": "module", "title": "模块", "width": "12%"},
                {"key": "reporter", "title": "报告人", "width": "10%"},
                {"key": "status", "title": "状态", "width": "10%"},
            ],
            data=[
                {"id": "BUG-001", "title": "登录页面502错误", "severity": "严重", "module": "网关", "reporter": "QA-Test", "status": "修复中"},
                {"id": "BUG-002", "title": "用户头像上传失败", "severity": "一般", "module": "用户", "reporter": "User-Report", "status": "待确认"},
                {"id": "BUG-003", "title": "搜索分页偏移错误", "severity": "一般", "module": "搜索", "reporter": "QA-Test", "status": "已确认"},
            ],
            order=4,
        ))

        template.add_component(MetricCardComponent(
            id="bug_metric_open",
            value="3",
            label="待修复",
            prefix="",
            suffix="个",
            trend="down",
            size="small",
            order=5,
        ))

        template.add_component(MetricCardComponent(
            id="bug_metric_critical",
            value="1",
            label="严重Bug",
            prefix="",
            suffix="个",
            trend="up",
            size="small",
            order=6,
        ))

        template.add_component(ProgressBarComponent(
            id="bug_progress",
            title="修复进度",
            percentage=65.0,
            style="bar",
            color="#52C41A",
            show_label=True,
            order=7,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 12. release_board - 发布看板
    # ============================================================
    @staticmethod
    def _create_release_board_components() -> list:
        template = PageTemplate(
            name="release_board",
            display_name="发布看板",
            icon="release",
            category="code",
            description="版本发布规划与追踪看板",
        )
        template.add_component(TextBlockComponent(
            id="release_title", content="发布看板", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="release_desc",
            content="版本发布计划、任务进度和发布检查清单。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(TimelineComponent(
            id="release_timeline",
            title="发布时间线",
            events=[
                {"id": "v1", "title": "v1.0 MVP", "description": "基础认证与用户管理", "date": "2026-01-15", "color": "#1890FF"},
                {"id": "v2", "title": "v1.1 功能增强", "description": "订单与支付系统", "date": "2026-02-28", "color": "#52C41A"},
                {"id": "v3", "title": "v2.0 重大更新", "description": "社交与推荐系统", "date": "2026-04-15", "color": "#722ED1"},
                {"id": "v4", "title": "v2.1 性能优化", "description": "缓存与数据库优化", "date": "2026-Q2", "color": "#FAAD14"},
            ],
            order=3,
        ))

        template.add_component(KanbanComponent(
            id="release_tasks",
            title="发布任务看板",
            columns=[
                {"id": "planned", "title": "已规划", "color": "#D9D9D9"},
                {"id": "in_progress", "title": "开发中", "color": "#1890FF"},
                {"id": "testing", "title": "测试中", "color": "#FAAD14"},
                {"id": "ready", "title": "就绪", "color": "#52C41A"},
            ],
            cards=[
                {"id": "t1", "title": "用户注册功能", "description": "v1.0 核心功能", "column_id": "ready", "priority": "high", "assignee": "Alice"},
                {"id": "t2", "title": "订单列表API", "description": "v1.1 功能", "column_id": "testing", "priority": "high", "assignee": "Bob"},
                {"id": "t3", "title": "支付对接", "description": "v1.1 关键功能", "column_id": "in_progress", "priority": "high", "assignee": "Charlie"},
                {"id": "t4", "title": "推荐算法", "description": "v2.0 新功能", "column_id": "planned", "priority": "medium", "assignee": ""},
            ],
            order=4,
        ))

        template.add_component(TableComponent(
            id="release_checklist",
            title="发布检查清单",
            columns=[
                {"key": "item", "title": "检查项", "width": "35%"},
                {"key": "status", "title": "状态", "width": "20%"},
                {"key": "responsible", "title": "责任人", "width": "15%"},
                {"key": "note", "title": "备注", "width": "25%"},
            ],
            data=[
                {"item": "代码审查完成", "status": "已完成", "responsible": "Tech Lead", "note": ""},
                {"item": "测试用例全部通过", "status": "进行中", "responsible": "QA", "note": "覆盖率85%"},
                {"item": "API文档更新", "status": "待处理", "responsible": "Backend", "note": ""},
                {"item": "数据库迁移脚本", "status": "已完成", "responsible": "DBA", "note": "已验证"},
            ],
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 13. sprint_board - Sprint看板
    # ============================================================
    @staticmethod
    def _create_sprint_board_components() -> list:
        template = PageTemplate(
            name="sprint_board",
            display_name="Sprint 看板",
            icon="sprint",
            category="code",
            description="敏捷迭代看板与任务管理",
        )
        template.add_component(TextBlockComponent(
            id="sprint_title", content="Sprint 看板", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="sprint_desc",
            content="当前迭代的任务看板，用于团队敏捷开发和进度跟踪。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(KanbanComponent(
            id="sprint_kanban",
            title="Sprint 任务看板",
            columns=[
                {"id": "todo", "title": "待开始", "color": "#D9D9D9"},
                {"id": "in_progress", "title": "进行中", "color": "#1890FF"},
                {"id": "review", "title": "审查中", "color": "#FAAD14"},
                {"id": "done", "title": "已完成", "color": "#52C41A"},
            ],
            cards=[
                {"id": "st1", "title": "实现用户导出功能", "description": "支持CSV/Excel导出", "column_id": "in_progress", "priority": "high", "assignee": "Alice"},
                {"id": "st2", "title": "修复搜索排序Bug", "description": "排序字段不正确", "column_id": "in_progress", "priority": "high", "assignee": "Bob"},
                {"id": "st3", "title": "添加请求限流", "description": "API限流中间件", "column_id": "todo", "priority": "medium", "assignee": "Charlie"},
                {"id": "st4", "title": "更新API文档", "description": "同步最新接口变更", "column_id": "review", "priority": "low", "assignee": "Alice"},
                {"id": "st5", "title": "编写单元测试", "description": "核心模块测试覆盖", "column_id": "done", "priority": "medium", "assignee": "Bob"},
            ],
            order=3,
        ))

        template.add_component(ProgressBarComponent(
            id="sprint_progress",
            title="Sprint 进度",
            percentage=62.0,
            style="dashboard",
            color="#1890FF",
            show_label=True,
            order=4,
        ))

        template.add_component(MetricCardComponent(
            id="sprint_metric_story",
            value="8",
            label="故事点数",
            prefix="共",
            suffix="点",
            size="small",
            order=5,
        ))

        template.add_component(MetricCardComponent(
            id="sprint_metric_completed",
            value="5",
            label="已完成",
            prefix="",
            suffix="点",
            trend="up",
            size="small",
            order=6,
        ))

        template.add_component(ListComponent(
            id="sprint_backlog",
            title="Sprint Backlog",
            items=[
                {"label": "优先级高", "value": "3个任务", "description": "核心功能和Bug修复", "icon": "priority"},
                {"label": "优先级中", "value": "2个任务", "description": "功能增强", "icon": "priority"},
                {"label": "优先级低", "value": "2个任务", "description": "文档和技术改进", "icon": "priority"},
            ],
            list_type="property",
            order=7,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 14. pr_tracker - PR追踪
    # ============================================================
    @staticmethod
    def _create_pr_tracker_components() -> list:
        template = PageTemplate(
            name="pr_tracker",
            display_name="PR 追踪",
            icon="pr",
            category="code",
            description="Pull Request 追踪与审查管理",
        )
        template.add_component(TextBlockComponent(
            id="pr_title", content="PR 追踪", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="pr_desc",
            content="跟踪所有 Pull Request 的状态、审查进度和合并情况。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(TableComponent(
            id="pr_table",
            title="PR 列表",
            columns=[
                {"key": "number", "title": "编号", "width": "8%"},
                {"key": "title", "title": "标题", "width": "25%"},
                {"key": "branch", "title": "分支", "width": "15%"},
                {"key": "author", "title": "作者", "width": "10%"},
                {"key": "reviewers", "title": "审查人", "width": "12%"},
                {"key": "status", "title": "状态", "width": "10%"},
            ],
            data=[
                {"number": "#45", "title": "feat: 添加通知模块", "branch": "feat/notification", "author": "Alice", "reviewers": "Bob, Charlie", "status": "待审查"},
                {"number": "#44", "title": "fix: 修复并发写入问题", "branch": "fix/concurrent-write", "author": "Bob", "reviewers": "Alice", "status": "审查中"},
                {"number": "#43", "title": "refactor: 抽取公共组件", "branch": "refactor/common", "author": "Charlie", "reviewers": "Alice, Bob", "status": "已合并"},
                {"number": "#42", "title": "docs: 更新部署文档", "branch": "docs/deploy", "author": "Alice", "reviewers": "", "status": "草稿"},
            ],
            order=3,
        ))

        template.add_component(ListComponent(
            id="pr_checklist",
            title="PR 审查清单",
            items=[
                {"label": "变更是否符合项目规范", "value": "编码风格检查", "description": "使用ESLint/PEP8", "icon": "checklist"},
                {"label": "是否包含测试代码", "value": "测试覆盖检查", "description": "新增代码应有对应测试", "icon": "checklist"},
                {"label": "是否更新文档", "value": "文档同步检查", "description": "API变更需更新文档", "icon": "checklist"},
                {"label": "是否存在冲突", "value": "合并冲突检查", "description": "需要无冲突合并", "icon": "checklist"},
            ],
            list_type="definition",
            order=4,
        ))

        template.add_component(MetricCardComponent(
            id="pr_metric_open",
            value="4",
            label="进行中",
            prefix="",
            suffix="个PR",
            trend="up",
            size="small",
            order=5,
        ))

        template.add_component(TimelineComponent(
            id="pr_activity",
            title="PR 动态",
            events=[
                {"id": "pe1", "title": "#45 创建", "description": "Alice 提交了通知模块PR", "date": "2026-01-10", "color": "#1890FF"},
                {"id": "pe2", "title": "#44 进入审查", "description": "Bob 修复并发写入问题", "date": "2026-01-09", "color": "#FAAD14"},
                {"id": "pe3", "title": "#43 已合并", "description": "Charlie 的公共组件重构", "date": "2026-01-08", "color": "#52C41A"},
            ],
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 15. changelog - 变更日志
    # ============================================================
    @staticmethod
    def _create_changelog_components() -> list:
        template = PageTemplate(
            name="changelog",
            display_name="变更日志",
            icon="changelog",
            category="code",
            description="版本变更历史与更新日志",
        )
        template.add_component(TextBlockComponent(
            id="changelog_title", content="变更日志", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="changelog_desc",
            content="项目各版本的详细变更记录，包括新功能、修复和改进。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(ChangelogComponent(
            id="changelog_entries",
            title="版本变更记录",
            entries=[
                {"version": "v2.1.0", "date": "2026-01-10", "type": "added", "description": "新增通知推送模块", "author": "Alice"},
                {"version": "v2.1.0", "date": "2026-01-10", "type": "modified", "description": "优化用户列表查询性能", "author": "Bob"},
                {"version": "v2.0.1", "date": "2026-01-05", "type": "fixed", "description": "修复并发写入导致的数据不一致问题", "author": "Bob"},
                {"version": "v2.0.0", "date": "2025-12-20", "type": "added", "description": "正式发布v2.0，新增社交互动模块", "author": "Team"},
                {"version": "v1.1.0", "date": "2025-11-15", "type": "added", "description": "新增订单系统和支付对接功能", "author": "Team"},
                {"version": "v1.0.1", "date": "2025-11-01", "type": "fixed", "description": "修复多项安全漏洞", "author": "Security Team"},
                {"version": "v1.0.0", "date": "2025-10-15", "type": "added", "description": "首次正式发布", "author": "Team"},
            ],
            order=3,
        ))

        template.add_component(TimelineComponent(
            id="changelog_timeline",
            title="版本时间线",
            events=[
                {"id": "cl1", "title": "v1.0.0", "description": "首次正式发布", "date": "2025-10", "color": "#1890FF"},
                {"id": "cl2", "title": "v1.1.0", "description": "订单与支付系统", "date": "2025-11", "color": "#52C41A"},
                {"id": "cl3", "title": "v2.0.0", "description": "社交互动大版本", "date": "2025-12", "color": "#722ED1"},
                {"id": "cl4", "title": "v2.1.0", "description": "通知与性能优化", "date": "2026-01", "color": "#FAAD14"},
            ],
            order=4,
        ))

        template.add_component(TableComponent(
            id="changelog_stats",
            title="版本统计",
            columns=[
                {"key": "version", "title": "版本", "width": "15%"},
                {"key": "date", "title": "日期", "width": "15%"},
                {"key": "additions", "title": "新增", "width": "15%"},
                {"key": "modifications", "title": "修改", "width": "15%"},
                {"key": "fixes", "title": "修复", "width": "15%"},
                {"key": "summary", "title": "概要", "width": "25%"},
            ],
            data=[
                {"version": "v2.1.0", "date": "2026-01-10", "additions": "3", "modifications": "5", "fixes": "2", "summary": "通知模块+性能优化"},
                {"version": "v2.0.0", "date": "2025-12-20", "additions": "12", "modifications": "8", "fixes": "4", "summary": "社交互动大版本"},
                {"version": "v1.1.0", "date": "2025-11-15", "additions": "6", "modifications": "3", "fixes": "1", "summary": "订单支付模块"},
                {"version": "v1.0.0", "date": "2025-10-15", "additions": "20", "modifications": "0", "fixes": "0", "summary": "初始版本"},
            ],
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 16. milestone_board - 里程碑看板
    # ============================================================
    @staticmethod
    def _create_milestone_board_components() -> list:
        template = PageTemplate(
            name="milestone_board",
            display_name="里程碑看板",
            icon="milestone",
            category="code",
            description="项目里程碑规划与进度追踪",
        )
        template.add_component(TextBlockComponent(
            id="milestone_title", content="里程碑看板", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="milestone_desc",
            content="关键里程碑节点、交付成果和当前进度。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(TimelineComponent(
            id="milestone_timeline",
            title="里程碑时间线",
            events=[
                {"id": "m1", "title": "原型完成", "description": "核心功能原型验证", "date": "2025-11", "color": "#1890FF"},
                {"id": "m2", "title": "Alpha内测", "description": "内部测试版本发布", "date": "2025-12", "color": "#52C41A"},
                {"id": "m3", "title": "Beta公测", "description": "公开测试版本", "date": "2026-02", "color": "#FAAD14"},
                {"id": "m4", "title": "正式发布", "description": "GA版本上线", "date": "2026-Q2", "color": "#EB2F96"},
            ],
            order=3,
        ))

        template.add_component(TableComponent(
            id="milestone_tasks",
            title="里程碑任务",
            columns=[
                {"key": "milestone", "title": "里程碑", "width": "15%"},
                {"key": "task", "title": "任务", "width": "30%"},
                {"key": "status", "title": "状态", "width": "12%"},
                {"key": "deadline", "title": "截止日期", "width": "15%"},
                {"key": "owner", "title": "负责人", "width": "10%"},
            ],
            data=[
                {"milestone": "原型完成", "task": "核心API开发", "status": "已完成", "deadline": "2025-11-15", "owner": "Alice"},
                {"milestone": "原型完成", "task": "前端原型实现", "status": "已完成", "deadline": "2025-11-20", "owner": "Bob"},
                {"milestone": "Alpha内测", "task": "集成测试", "status": "进行中", "deadline": "2025-12-20", "owner": "Charlie"},
                {"milestone": "Beta公测", "task": "性能优化", "status": "待开始", "deadline": "2026-02-01", "owner": "Alice"},
            ],
            order=4,
        ))

        template.add_component(ProgressBarComponent(
            id="milestone_progress",
            title="总体完成进度",
            percentage=45.0,
            style="bar",
            color="#722ED1",
            show_label=True,
            order=5,
        ))

        template.add_component(MetricCardComponent(
            id="milestone_metric_completed",
            value="1",
            label="已完成",
            prefix="",
            suffix="/4",
            size="small",
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 17. feature_status - 功能状态
    # ============================================================
    @staticmethod
    def _create_feature_status_components() -> list:
        template = PageTemplate(
            name="feature_status",
            display_name="功能状态",
            icon="feature",
            category="code",
            description="功能模块开发状态总览",
        )
        template.add_component(TextBlockComponent(
            id="feature_title", content="功能状态", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="feature_desc",
            content="各功能模块的开发状态、完成进度和负责人信息。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(KanbanComponent(
            id="feature_kanban",
            title="功能开发看板",
            columns=[
                {"id": "planned", "title": "规划中", "color": "#D9D9D9"},
                {"id": "developing", "title": "开发中", "color": "#1890FF"},
                {"id": "testing", "title": "测试中", "color": "#FAAD14"},
                {"id": "launched", "title": "已上线", "color": "#52C41A"},
            ],
            cards=[
                {"id": "f1", "title": "用户管理模块", "description": "注册/登录/资料管理", "column_id": "launched", "priority": "high", "assignee": "Alice"},
                {"id": "f2", "title": "订单系统", "description": "下单/支付/退款", "column_id": "testing", "priority": "high", "assignee": "Bob"},
                {"id": "f3", "title": "消息通知", "description": "站内信/推送/邮件", "column_id": "developing", "priority": "medium", "assignee": "Charlie"},
                {"id": "f4", "title": "数据分析", "description": "用户行为统计报表", "column_id": "planned", "priority": "low", "assignee": ""},
            ],
            order=3,
        ))

        template.add_component(MetricCardComponent(
            id="feature_metric_total",
            value="12",
            label="总功能数",
            prefix="",
            suffix="个",
            size="small",
            order=4,
        ))

        template.add_component(MetricCardComponent(
            id="feature_metric_launched",
            value="6",
            label="已上线",
            prefix="",
            suffix="个",
            trend="up",
            size="small",
            order=5,
        ))

        template.add_component(ProgressBarComponent(
            id="feature_progress",
            title="总体完成率",
            percentage=50.0,
            style="circle",
            color="#1890FF",
            show_label=True,
            order=6,
        ))

        template.add_component(ListComponent(
            id="feature_list",
            title="功能清单",
            items=[
                {"label": "用户管理", "value": "100%", "description": "注册、登录、资料管理，已上线", "icon": "feature"},
                {"label": "订单系统", "value": "80%", "description": "下单、支付功能，测试中", "icon": "feature"},
                {"label": "消息通知", "value": "45%", "description": "站内信功能，开发中", "icon": "feature"},
                {"label": "数据分析", "value": "10%", "description": "统计报表，规划中", "icon": "feature"},
            ],
            list_type="property",
            order=7,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 18. release_notes_editor - 发布说明编辑器
    # ============================================================
    @staticmethod
    def _create_release_notes_editor_components() -> list:
        template = PageTemplate(
            name="release_notes_editor",
            display_name="发布说明",
            icon="notes",
            category="code",
            description="版本发布说明编辑与预览",
        )
        template.add_component(TextBlockComponent(
            id="notes_title", content="发布说明", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="notes_desc",
            content="编辑和预览版本发布说明，包含新功能、修复和改进的描述。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(ChangelogComponent(
            id="notes_changelog",
            title="当前版本变更",
            entries=[
                {"version": "v2.1.0", "date": "2026-01-10", "type": "added", "description": "新增通知推送模块，支持站内信和邮件通知", "author": "Alice"},
                {"version": "v2.1.0", "date": "2026-01-10", "type": "modified", "description": "优化用户列表API查询性能，响应时间降低60%", "author": "Bob"},
                {"version": "v2.1.0", "date": "2026-01-10", "type": "fixed", "description": "修复高并发下订单创建重复问题", "author": "Charlie"},
                {"version": "v2.1.0", "date": "2026-01-10", "type": "security", "description": "升级依赖库修复已知安全漏洞", "author": "Security"},
            ],
            order=3,
        ))

        template.add_component(ListComponent(
            id="notes_summary",
            title="变更摘要",
            items=[
                {"label": "新功能", "value": "1个", "description": "通知推送模块", "icon": "plus", "checked": True},
                {"label": "改进", "value": "3项", "description": "性能优化和体验提升", "icon": "up", "checked": True},
                {"label": "Bug修复", "value": "2个", "description": "关键问题修复", "icon": "fix", "checked": True},
                {"label": "安全更新", "value": "1项", "description": "依赖库安全升级", "icon": "shield", "checked": True},
            ],
            list_type="definition",
            order=4,
        ))

        template.add_component(TagSetComponent(
            id="notes_tags",
            tags=[
                {"name": "v2.1.0", "color": "#1890FF", "count": 1},
                {"name": "stable", "color": "#52C41A", "count": 1},
                {"name": "feature", "color": "#722ED1", "count": 1},
            ],
            allow_create=True,
            order=5,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 19. ops_manual - 运维手册
    # ============================================================
    @staticmethod
    def _create_ops_manual_components() -> list:
        template = PageTemplate(
            name="ops_manual",
            display_name="运维手册",
            icon="ops",
            category="code",
            description="系统运维与操作手册",
        )
        template.add_component(TextBlockComponent(
            id="ops_title", content="运维手册", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="ops_desc",
            content="系统运维操作指南，包括服务启停、监控告警、故障处理和备份恢复。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(StepsComponent(
            id="ops_startup",
            title="服务启动流程",
            steps=[
                {"id": "o1", "title": "检查依赖服务", "description": "确认数据库、缓存服务运行正常", "status": "completed"},
                {"id": "o2", "title": "启动应用服务", "description": "运行 docker-compose up -d", "status": "completed"},
                {"id": "o3", "title": "健康检查", "description": "访问 /health 端点确认", "status": "in_progress"},
                {"id": "o4", "title": "流量接入", "description": "打开负载均衡流量", "status": "pending"},
            ],
            current=2,
            order=3,
        ))

        template.add_component(TableComponent(
            id="ops_commands",
            title="常用运维命令",
            columns=[
                {"key": "purpose", "title": "用途", "width": "25%"},
                {"key": "command", "title": "命令", "width": "45%"},
                {"key": "note", "title": "备注", "width": "25%"},
            ],
            data=[
                {"purpose": "查看服务状态", "command": "docker-compose ps", "note": "查看所有容器状态"},
                {"purpose": "查看日志", "command": "docker-compose logs -f app", "note": "实时跟踪日志"},
                {"purpose": "重启服务", "command": "docker-compose restart app", "note": "不中断其他服务"},
                {"purpose": "数据备份", "command": "pg_dump db > backup.sql", "note": "定期备份数据库"},
            ],
            order=4,
        ))

        template.add_component(TextBlockComponent(
            id="ops_script",
            content='''# 部署脚本示例
#!/bin/bash
set -e

echo "=== 开始部署 ==="

# 拉取最新代码
git pull origin main

# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 健康检查
sleep 5
curl -f http://localhost:8000/health && echo "部署成功" || echo "部署失败"''',
            sub_type="code_block", language="bash", title="部署脚本", order=5,
        ))

        template.add_component(ListComponent(
            id="ops_contacts",
            title="运维联系人",
            items=[
                {"label": "系统管理员", "value": "Alice", "description": "负责服务器和基础设施", "icon": "contact"},
                {"label": "数据库管理员", "value": "Bob", "description": "负责数据库运维", "icon": "contact"},
                {"label": "安全负责人", "value": "Charlie", "description": "负责安全审计", "icon": "contact"},
            ],
            list_type="property",
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # 20. prd - 产品需求文档
    # ============================================================
    @staticmethod
    def _create_prd_components() -> list:
        template = PageTemplate(
            name="prd",
            display_name="产品需求文档",
            icon="prd",
            category="code",
            description="产品需求定义与功能规格说明",
        )
        template.add_component(TextBlockComponent(
            id="prd_title", content="产品需求文档", sub_type="heading", level=1, order=0,
        ))
        template.add_component(TextBlockComponent(
            id="prd_desc",
            content="产品需求定义文档，包括业务目标、功能规格和非功能需求。",
            sub_type="paragraph", order=1,
        ))
        template.add_component(DividerComponent(order=2))

        template.add_component(ListComponent(
            id="prd_requirements",
            title="需求清单",
            items=[
                {"label": "PRD-REQ-001", "value": "用户认证", "description": "支持邮箱/手机号注册、登录、密码重置", "icon": "req", "checked": True},
                {"label": "PRD-REQ-002", "value": "用户资料", "description": "个人资料编辑、头像上传", "icon": "req", "checked": True},
                {"label": "PRD-REQ-003", "value": "商品浏览", "description": "商品列表搜索、筛选、详情查看", "icon": "req", "checked": False},
                {"label": "PRD-REQ-004", "value": "下单购买", "description": "购物车、下单、支付", "icon": "req", "checked": False},
                {"label": "PRD-REQ-005", "value": "订单管理", "description": "订单列表、详情、退款", "icon": "req", "checked": False},
            ],
            list_type="definition",
            show_checkbox=True,
            order=3,
        ))

        template.add_component(TableComponent(
            id="prd_specs",
            title="功能规格表",
            columns=[
                {"key": "feature", "title": "功能", "width": "20%"},
                {"key": "description", "title": "描述", "width": "30%"},
                {"key": "priority", "title": "优先级", "width": "10%"},
                {"key": "effort", "title": "预估工时", "width": "10%"},
                {"key": "dependencies", "title": "依赖", "width": "15%"},
            ],
            data=[
                {"feature": "用户注册", "description": "邮箱注册+验证码验证", "priority": "P0", "effort": "3d", "dependencies": "邮件服务"},
                {"feature": "用户登录", "description": "支持JWT令牌认证", "priority": "P0", "effort": "2d", "dependencies": ""},
                {"feature": "商品搜索", "description": "全文搜索+分类筛选", "priority": "P1", "effort": "5d", "dependencies": "搜索引擎"},
                {"feature": "在线支付", "description": "对接微信/支付宝", "priority": "P1", "effort": "8d", "dependencies": "支付网关"},
                {"feature": "订单退款", "description": "退款流程与审核", "priority": "P2", "effort": "3d", "dependencies": "订单系统"},
            ],
            order=4,
        ))

        template.add_component(KanbanComponent(
            id="prd_priority",
            title="需求优先级看板",
            columns=[
                {"id": "p0", "title": "P0 必须完成", "color": "#EB2F96"},
                {"id": "p1", "title": "P1 应该完成", "color": "#FAAD14"},
                {"id": "p2", "title": "P2 可以完成", "color": "#1890FF"},
                {"id": "p3", "title": "P3 未来考虑", "color": "#D9D9D9"},
            ],
            cards=[
                {"id": "pc1", "title": "用户注册登录", "description": "MVP核心认证流程", "column_id": "p0", "priority": "urgent", "assignee": "Alice"},
                {"id": "pc2", "title": "商品搜索浏览", "description": "商品列表与搜索", "column_id": "p1", "priority": "high", "assignee": "Bob"},
                {"id": "pc3", "title": "在线支付对接", "description": "支付渠道集成", "column_id": "p1", "priority": "high", "assignee": "Charlie"},
                {"id": "pc4", "title": "推荐系统", "description": "个性化商品推荐", "column_id": "p3", "priority": "low", "assignee": ""},
            ],
            order=5,
        ))

        template.add_component(TagSetComponent(
            id="prd_tags",
            tags=[
                {"name": "P0", "color": "#EB2F96", "count": 2},
                {"name": "P1", "color": "#FAAD14", "count": 4},
                {"name": "P2", "color": "#1890FF", "count": 3},
                {"name": "MVP", "color": "#52C41A", "count": 1},
            ],
            allow_create=True,
            order=6,
        ))

        template.add_component(SpacerComponent(height=24, order=999))
        return template.get_default_schema()["components"]

    # ============================================================
    # PAGE_TYPES 字典 - 将所有页面类型注册到此处
    # ============================================================
    PAGE_TYPES = {
        "system_arch": {
            "name": "system_arch",
            "display_name": "系统架构",
            "icon": "architecture",
            "category": "code",
            "description": "系统整体架构设计与服务关系图",
            "default_schema": {
                "components": _create_system_arch_components.__func__(),
            }
        },
        "api_definition": {
            "name": "api_definition",
            "display_name": "API 定义",
            "icon": "api",
            "category": "code",
            "description": "API 接口定义与文档",
            "default_schema": {
                "components": _create_api_definition_components.__func__(),
            }
        },
        "data_model": {
            "name": "data_model",
            "display_name": "数据模型",
            "icon": "database",
            "category": "code",
            "description": "数据库表结构设计与实体关系",
            "default_schema": {
                "components": _create_data_model_components.__func__(),
            }
        },
        "tech_selection": {
            "name": "tech_selection",
            "display_name": "技术选型",
            "icon": "selection",
            "category": "code",
            "description": "技术方案选型与对比分析",
            "default_schema": {
                "components": _create_tech_selection_components.__func__(),
            }
        },
        "user_story_map": {
            "name": "user_story_map",
            "display_name": "用户故事地图",
            "icon": "story_map",
            "category": "code",
            "description": "用户故事地图与需求优先级规划",
            "default_schema": {
                "components": _create_user_story_map_components.__func__(),
            }
        },
        "test_case_set": {
            "name": "test_case_set",
            "display_name": "测试用例集",
            "icon": "test_case",
            "category": "code",
            "description": "单元测试与集成测试用例管理",
            "default_schema": {
                "components": _create_test_case_set_components.__func__(),
            }
        },
        "deploy_flow": {
            "name": "deploy_flow",
            "display_name": "部署流程",
            "icon": "deploy",
            "category": "code",
            "description": "CI/CD 部署流水线与环境管理",
            "default_schema": {
                "components": _create_deploy_flow_components.__func__(),
            }
        },
        "tech_debt": {
            "name": "tech_debt",
            "display_name": "技术债务",
            "icon": "tech_debt",
            "category": "code",
            "description": "技术债务追踪与管理",
            "default_schema": {
                "components": _create_tech_debt_components.__func__(),
            }
        },
        "code_review_list": {
            "name": "code_review_list",
            "display_name": "代码审查清单",
            "icon": "code_review",
            "category": "code",
            "description": "代码审查清单与评审追踪",
            "default_schema": {
                "components": _create_code_review_list_components.__func__(),
            }
        },
        "code_snippet_lib": {
            "name": "code_snippet_lib",
            "display_name": "代码片段库",
            "icon": "snippet",
            "category": "code",
            "description": "常用代码片段与工具函数库",
            "default_schema": {
                "components": _create_code_snippet_lib_components.__func__(),
            }
        },
        "bug_tracker": {
            "name": "bug_tracker",
            "display_name": "Bug 追踪",
            "icon": "bug",
            "category": "code",
            "description": "Bug 缺陷追踪与修复管理",
            "default_schema": {
                "components": _create_bug_tracker_components.__func__(),
            }
        },
        "release_board": {
            "name": "release_board",
            "display_name": "发布看板",
            "icon": "release",
            "category": "code",
            "description": "版本发布规划与追踪看板",
            "default_schema": {
                "components": _create_release_board_components.__func__(),
            }
        },
        "sprint_board": {
            "name": "sprint_board",
            "display_name": "Sprint 看板",
            "icon": "sprint",
            "category": "code",
            "description": "敏捷迭代看板与任务管理",
            "default_schema": {
                "components": _create_sprint_board_components.__func__(),
            }
        },
        "pr_tracker": {
            "name": "pr_tracker",
            "display_name": "PR 追踪",
            "icon": "pr",
            "category": "code",
            "description": "Pull Request 追踪与审查管理",
            "default_schema": {
                "components": _create_pr_tracker_components.__func__(),
            }
        },
        "changelog": {
            "name": "changelog",
            "display_name": "变更日志",
            "icon": "changelog",
            "category": "code",
            "description": "版本变更历史与更新日志",
            "default_schema": {
                "components": _create_changelog_components.__func__(),
            }
        },
        "milestone_board": {
            "name": "milestone_board",
            "display_name": "里程碑看板",
            "icon": "milestone",
            "category": "code",
            "description": "项目里程碑规划与进度追踪",
            "default_schema": {
                "components": _create_milestone_board_components.__func__(),
            }
        },
        "feature_status": {
            "name": "feature_status",
            "display_name": "功能状态",
            "icon": "feature",
            "category": "code",
            "description": "功能模块开发状态总览",
            "default_schema": {
                "components": _create_feature_status_components.__func__(),
            }
        },
        "release_notes_editor": {
            "name": "release_notes_editor",
            "display_name": "发布说明",
            "icon": "notes",
            "category": "code",
            "description": "版本发布说明编辑与预览",
            "default_schema": {
                "components": _create_release_notes_editor_components.__func__(),
            }
        },
        "ops_manual": {
            "name": "ops_manual",
            "display_name": "运维手册",
            "icon": "ops",
            "category": "code",
            "description": "系统运维与操作手册",
            "default_schema": {
                "components": _create_ops_manual_components.__func__(),
            }
        },
        "prd": {
            "name": "prd",
            "display_name": "产品需求文档",
            "icon": "prd",
            "category": "code",
            "description": "产品需求定义与功能规格说明",
            "default_schema": {
                "components": _create_prd_components.__func__(),
            }
        },
    }
