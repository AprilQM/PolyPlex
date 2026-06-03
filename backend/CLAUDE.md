# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PolyPlex is a collaboration platform for inspiration curation and project co-creation. It features Git-style branch/version management applied to creative projects, AI-assisted project generation, and modular page-component architecture.

**Stack**: FastAPI + SQLAlchemy async + MySQL (asyncmy) + Snowflake IDs + Redis + ChromaDB + LangChain

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python main.py          # Default: 0.0.0.0:8000

# Database migrations (Alembic)
alembic revision --autogenerate -m "description"
alembic upgrade head

# Tests
pytest
pytest tests/test_branches.py
```

## Architecture

### Layered Structure (strict 4-layer, top-down only)

```
Client → app/api/ → app/services/ → app/crud/ → app/models/ → MySQL
```

- **api/** — FastAPI route definitions, parameter validation, no business logic
- **services/** — Business logic, external service integrations (AI, RAG, notifications)
- **crud/** — Database operations. Each function takes `AsyncSession` as first param, commits internally
- **models/** — SQLAlchemy ORM models (declarative base, async engine)

### Directory Layout

| Directory | Purpose |
|-----------|---------|
| `app/api/` | API route definitions (file.py currently, more expected) |
| `app/core/` | Core config: database.py (async MySQL engine, session factory, auto-DB-creation on startup) |
| `app/models/` | 9 model files across users, projects, pages, branches, versions, components, merge_requests, members, files, notifications |
| `app/crud/` | 11 CRUD modules — 1:1 with model groups (users, projects, pages, components, branches, branch_versions, merge_requests, project_members, files, file_packages, notifications) |
| `app/schemas/` | Pydantic request/response schemas (planned, see md说明文档/项目结构.md) |
| `app/services/` | Business logic layer (file_service.py, component_service.py) |
| `app/middleware/` | Auth, logging, error handling middleware (planned, dir exists) |
| `app/utils/` | Snowflake ID generator (all entity IDs), validators, helpers |
| `app/page_components/` | 48 component classes across 8 categories (basic, structured, visualization, metric, collaboration, reference, domain_specific, utility) |
| `app/project_templates/` | 97 page templates across 12 domains (code, writing, design, business, lifestyle, academic, media, education, marketing, music, general, other) |

### Key Design Decisions

1. **Snowflake IDs** — All primary keys use typed Snowflake IDs (app/utils/snowflake.py). 19 entity types with 5-bit type discriminator, 7-bit sequence, millisecond-precision timestamp. IDs embedded in the binary, not auto-increment.

2. **Git-style versioning** — Branches, versions (commits), diffs, and merge requests mirror Git semantics. `BranchVersion` tracks per-page changes with component-level granularity. `BranchVersionChange` records create/update/delete per page per version.

3. **Component system** — 48 component types with an abstract `Component` base class (ABC). Each component implements `get_data()` and `get_schema()`. Components are composed into pages via `PageComponentRelation` (order_index).

4. **Page templates** — 97 predefined page templates across 12 domains. Each template is a `PageTemplate` object composing multiple `Component` instances. Templates are registered in `project_templates/*.py` and aggregated in `project_templates/__init__.py`.

5. **Async everything** — All DB operations use SQLAlchemy async engine + `AsyncSession`. CRUD functions are `async def` throughout.

### Core Data Flow

```
Project → Branch(es) → BranchVersion(commits) → BranchVersionChange(diff per page)
Project → ProjectPage(s) → Component(s) via PageComponentRelation
Project → ProjectMember(s) with RoleType (OWNER/ADMIN/CONTRIBUTOR/VIEWER)
```

### Import Pattern

All models re-exported from `app.models.__init__`, all CRUD functions from `app.crud.__init__`, all components from `app.page_components.__init__`, all template lookups from `app.project_templates.__init__`. Import from the package, not individual files.

```python
from app.crud import get_project, get_page, create_component
from app.models import Project, ProjectPage, Component, Branch
from app.page_components import TextBlockComponent, ComponentType
from app.project_templates import ALL_PAGE_TYPES, get_page_type_info
```

### CRUD Convention

- All functions accept `db: AsyncSession` as the first parameter
- Each function handles its own `commit()` internally (exception: `sync_page_components` manages its own transaction via `db.begin()`)
- Return the ORM object or None (not HTTP exceptions)
- `@validate_args` decorator used in some modules for type coercion
