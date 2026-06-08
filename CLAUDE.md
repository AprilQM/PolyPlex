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
npm run dev                             # Vite dev server (localhost:5173)
npm run build                           # Production build → frontend/dist/
npm run preview                         # Preview production build

# All-in-one (requires nginx/ + dist/)
.\manage.ps1 start                      # Start backend + frontend + nginx
.\manage.ps1 stop                       # Stop all
.\manage.ps1 status                     # Show running status
.\manage.ps1 kill-port 8000             # Kill process on port 8000

# Tests (backend)
cd backend
pytest                                  # Run all tests
pytest tests/test_auth_flow.py -v       # Single test file
```

Backend: `0.0.0.0:8000` (FastAPI + uvicorn). Frontend dev: `localhost:5173` (Vite). Production: nginx `localhost:80` reverse-proxies API to backend and serves SPA from `frontend/dist/`.

## Monorepo Layout

```
PolyPlex/
├── backend/
│   ├── main.py                         # FastAPI app entry, lifespan auto-creates DB + system user
│   ├── requirements.txt
│   ├── .env.example                    # Environment variable template
│   └── app/
│       ├── api/                        # FastAPI route definitions (thin layer, no business logic)
│       ├── core/                       # database, auth/JWT, redis_client, rsa_key, email, git_config
│       ├── models/                     # SQLAlchemy ORM models (users, projects, pages, branches, versions, components, merge_requests, members, files, groups, notifications)
│       ├── crud/                       # DB operations (1:1 with model groups, 15 modules)
│       ├── services/                   # Business logic (branch, component, file, file_access, git)
│       ├── page_components/            # 48 component classes across 8 categories (ABC base class)
│       └── project_templates/          # 97 page templates across 12 domains
├── frontend/
│   └── src/
│       ├── main.js                     # Vue app entry (Pinia + router setup)
│       ├── App.vue                     # Root component (<router-view />)
│       ├── router/index.js             # Routes: /home, /workbench/*, /form/*, /admin
│       ├── stores/                     # Pinia stores (useUserStore, useSecondaryNavStore)
│       ├── layouts/                    # WorkbenchLayout, FormLayout, AdminLayout
│       ├── views/                      # Home (landing), 6 workbench views, 3 form views
│       ├── components/                 # Reusable Vue components (nav, etc.)
│       ├── composables/                # url.js helper
│       └── styles/                     # Global CSS (index.css, font.css, color.css with design tokens)
├── nginx/
│   └── conf/nginx.conf                # Reverse proxy: API → :8000, SPA → frontend/dist/
├── tests/
│   └── test_auth_flow.py              # Auth flow integration tests
├── manage.ps1                         # Process manager (start/stop/restart/status/kill-port)
├── .gitignore
└── docs/superpowers/                  # Design docs and implementation plans
```

## Architecture — Backend

### 4-Layer Strict Layering (top-down only)

```
Client → app/api/ → app/services/ → app/crud/ → app/models/ → MySQL
```

- **api/** — FastAPI route handlers. Parameter validation only, no business logic. Routes call into services or directly into crud for simple operations.
- **services/** — Business logic layer. Orchestrates multi-step operations. Modules: `branch_service.py` (branch cloning, merge execution, commit), `file_service.py` (file upload with dedup), `component_service.py`, `file_access_service.py` (access control), `git_service.py` (Git HTTP Smart Protocol, refs/advertisement, pack upload).
- **crud/** — Database operations. Every function accepts `db: AsyncSession` as first param and commits internally. Return ORM objects or None (never HTTP errors).
- **models/** — SQLAlchemy declarative models. Use Snowflake IDs (typed, bigint) as primary keys. All timestamps are `BigInteger` (Unix epoch seconds).

### Auth & Core Infrastructure

- **RSA encryption** — Frontend encrypts passwords with `jsencrypt` (PKCS#1 v1.5) using backend's RSA public key. Backend decrypts with `cryptography` library. Keys auto-generated on first startup. See `app/core/rsa_key.py`.
- **Email verification** — Registration sends verification email via SMTP (QQ mail). Redis stores pending registrations with 30-min TTL. Verify-code endpoint activates user and returns JWT. See `app/core/email.py`, `app/api/auth.py` `POST /register`, `POST /verify-code`.
- **JWT auth** — `create_access_token()` in `app/core/auth.py`. Token contains `user_id`, `username`, `job_number`, `is_system`. Token-based auth check in router guard + `get_current_user` dependency.
- **Redis** — Used for email verification codes, rate limiting. Configured in `.env` (`REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`). See `app/core/redis_client.py`.
- **Git tokens** — Users have a `git_token_hash` column. Tokens are SHA-256 hashed, one-time display on generation. Used for Git HTTP Smart Protocol authentication.

### Git HTTP Backend

PolyPlex implements Git HTTP Smart Protocol at `/api/git/<repo>` supporting `git clone/push/fetch`. See `backend/app/api/git.py`:
- `GET /api/git/<repo>/info/refs?service=git-upload-pack` — Advertise refs (clone/fetch)
- `POST /api/git/<repo>/git-upload-pack` — Serve pack data (fetch)
- `POST /api/git/<repo>/git-receive-pack` — Accept pack data (push)
- Auth: Basic auth via username + git_token (falls back to password). Git repos stored under `FILE_PATH/git/`.

### Core Data Entities & Relationships

```
Project ──→ Branch(es) ──→ BranchVersion(commits) ──→ BranchVersionChange(diff per page)
Project ──→ ProjectPage(s) ──→ PageComponentRelation ──→ Component
Project ──→ ProjectMember(s) with RoleType (OWNER/ADMIN/CONTRIBUTOR/VIEWER)
Project ──→ ProjectTag(s) via ProjectTagRelation
File ──→ FilePackage(s) via FilePackageRelation
User ──→ UserTag(s) via UserTagRelation
User ──→ Group(s) via GroupUserRelation
File ──→ FileAccessControl(s) — permission-based file access
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
