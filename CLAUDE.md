# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PolyPlex is an AI-native collaboration platform for inspiration curation and project co-creation. It applies Git-style branch/version management to creative projects — users create branches to explore ideas, commit versions, and merge changes back. AI assists with project generation, page deepening, and version iteration.

**Stack**: FastAPI + SQLAlchemy async + MySQL (asyncmy) (backend) + Vue 3 + Pinia + vue-router + Vite (frontend)

## Commands

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py                          # Start server at 0.0.0.0:8000

# Frontend
cd frontend
npm install
npm run dev                             # Vite dev server
npm run build                           # Production build
npm run preview                         # Preview production build
```

Both servers run independently — backend on `0.0.0.0:8000` (FastAPI + uvicorn), frontend on Vite default (usually `localhost:5173`).

## Monorepo Layout

```
PolyPlex/
├── backend/
│   ├── main.py                         # FastAPI app entry, lifespan auto-creates DB + system user
│   ├── requirements.txt
│   └── app/
│       ├── api/                        # FastAPI route definitions (thin layer, no business logic)
│       ├── core/                       # database.py (async MySQL engine, session factory)
│       ├── models/                     # SQLAlchemy ORM models (9 model groups)
│       ├── crud/                       # DB operations (11 modules, 1:1 with models)
│       ├── services/                   # Business logic (branch_service, file_service, component_service)
│       ├── schemas/                    # Pydantic schemas (planned, dir exists)
│       ├── middleware/                 # Auth/logging/error middleware (planned, dir exists)
│       ├── utils/                      # Snowflake ID generator, hash utilities
│       ├── page_components/            # 48 component classes across 8 categories (ABC base class)
│       └── project_templates/          # 93 page templates across 12 domains
├── frontend/
│   └── src/
│       ├── main.js                     # Vue app entry (Pinia + router setup)
│       ├── App.vue                     # Root component (<router-view />)
│       ├── router/index.js             # Routes: /home, /workbench/*, /form/*, /admin
│       ├── stores/                     # Pinia stores (useUserStore, useSecondaryNavStore)
│       ├── layouts/                    # WorkbenchLayout, FormLayout, AdminLayout
│       ├── views/                      # Home (landing), workbench/*, form/* (Login/Register)
│       ├── components/                 # Reusable Vue components
│       ├── composables/                # Vue composables (empty/planned)
│       └── styles/                     # Global CSS (index.css, font.css, color.css)
```

## Architecture — Backend

### 4-Layer Strict Layering (top-down only)

```
Client → app/api/ → app/services/ → app/crud/ → app/models/ → MySQL
```

- **api/** — FastAPI route handlers. Parameter validation only, no business logic. Routes call into services or directly into crud for simple operations.
- **services/** — Business logic layer. Orchestrates multi-step operations (branch cloning, merge execution, file upload with dedup). Currently has `branch_service.py`, `file_service.py`, `component_service.py`.
- **crud/** — Database operations. Every function accepts `db: AsyncSession` as first param and commits internally. Return ORM objects or None (never HTTP errors).
- **models/** — SQLAlchemy declarative models. Use Snowflake IDs (typed, bigint) as primary keys. All timestamps are `BigInteger` (Unix epoch seconds).

### Core Data Entities & Relationships

```
Project ──→ Branch(es) ──→ BranchVersion(commits) ──→ BranchVersionChange(diff per page)
Project ──→ ProjectPage(s) ──→ PageComponentRelation ──→ Component
Project ──→ ProjectMember(s) with RoleType (OWNER/ADMIN/CONTRIBUTOR/VIEWER)
Project ──→ ProjectTag(s) via ProjectTagRelation
File ──→ FilePackage(s) via FilePackageRelation
User ──→ UserTag(s) via UserTagRelation
```

### Key Design Decisions

1. **Snowflake IDs** — All primary keys use typed Snowflake IDs. 19 entity types with a 5-bit type discriminator, 7-bit sequence, millisecond-precision timestamp. See `backend/app/utils/snowflake.py` for generators and type constants.

2. **Git-style versioning** — Branches (`BranchStatus: draft/pending/merged/rejected`), versions (commits with parent pointers), and merge requests (`MergeRequestStatus: pending/approved/rejected/merged`) mirror Git semantics. Service layer in `branch_service.py` provides high-level `commit()`, `commit_by_name()`, `create_branch_clone()`, and `execute_merge()` functions.

3. **Component system** — 48 component types with abstract `Component` base class (ABC) in `page_components/base.py`. Each component implements `get_data()` and `get_schema()`. Components are composed into pages via `PageComponentRelation` (order_index). Category breakdown: Basic(6) + Structured(5) + Visualization(6) + Metric(5) + Collaboration(4) + Reference(4) + Domain(13) + Utility(5).

4. **Page templates** — 93 predefined page templates across 12 domains (code, writing, design, business, lifestyle, academic, media, education, marketing, music, general, other). Each `PageTemplate` composes multiple `Component` instances. Registered via `project_templates/__init__.py` with lookup functions (`get_page_type_info`, `get_page_types_by_category`).

5. **Async everything** — All DB operations use SQLAlchemy async engine + `AsyncSession`. CRUD functions are `async def`. The `get_db()` dependency yields `AsyncSession`.

### Import Conventions

All models re-exported from `app.models.__init__`, all CRUD functions from `app.crud.__init__`, all components from `app.page_components.__init__`, all template lookups from `app.project_templates.__init__`. Import from the package, not individual files:

```python
from app.crud import get_project, create_component
from app.models import Project, Component, Branch
from app.page_components import TextBlockComponent, ComponentType
from app.project_templates import ALL_PAGE_TYPES, get_page_type_info
```

## Architecture — Frontend

### Route Structure

- `/home` — Landing page (hero, features, workflow, templates showcase)
- `/workbench/*` — Main app (requires auth via `router.beforeEach`, redirects to `/form/login` if no token)
  - `/workbench/dashboard` — Dashboard
  - `/workbench/square` — Project square/discovery
  - `/workbench/project-manage` — Project management
  - `/workbench/assist` — AI assist
  - `/workbench/user-space/:id` — User profile
  - `/workbench/notice` — Notifications
- `/form/login` and `/form/register` — Auth forms (FormLayout)
- `/admin/*` — Admin panel (AdminLayout, children TBD)

### Layouts

- **WorkbenchLayout** — Main app shell with topNav, leftNav (secondary nav), bottomNav, and `<router-view>`.
- **FormLayout** — Minimal wrapper for login/register pages.
- **AdminLayout** — Admin panel wrapper.

### State Management (Pinia)

- **useUserStore** — User info (id, username, email, avatar, isAdmin, isBan, token, messageCount). Token-based auth check in router guard.
- **useSecondaryNavStore** — Controls the secondary left navigation panel (width, content sections with buttons, animation state via `switchNew`).

### Secondary Nav Pattern

Each workbench view sets the secondary nav content and width on mount. The nav has sections (title + button groups). Buttons have `active` state, `icon`, `text`, and `command` handler. Navigation uses `switchGlobal` (deactivate all, activate one) or `switchInPart` (activate within section). Content swap animates via `_x` transform.

## Development Notes

- Backend auto-creates the MySQL database and system user on startup (see `main.py` lifespan).
- Frontend uses `@` path alias pointing to `frontend/src/`.
- `.env` file for backend config: `APP_HOST`, `APP_PORT`, `DATABASE_*`, `FILE_PATH`, `SYSTEM_USERNAME`, `SYSTEM_USER_PASSWORD`.
- Many workbench views are stubs (empty containers that set secondary nav state). The core logic is in the backend models, CRUD, services, and page template system.
- The project is in early development — many API routes, middleware, and frontend views are not yet implemented.
