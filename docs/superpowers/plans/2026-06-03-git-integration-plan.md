# Git Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Make PolyPlex a Git HTTP server where each project has a backing Git repository, file management stores files in the Git working tree, and Git clients can clone/push/pull via HTTP.

**Architecture:** Git working tree = file storage. Bare repo = Git protocol interface. File DB = metadata authority. Uploads write to worktree + commit. Push syncs to File DB.

**Tech Stack:** FastAPI + Git subprocess + MySQL asyncmy

---

### File Structure

| File | Responsibility |
|------|----------------|
| `app/core/git_config.py` (create) | GIT_REPO_DIR path config, path helpers for repo/worktree |
| `app/models/files.py` (modify) | Add `git_path` column to File model |
| `app/services/git_service.py` (create) | Git repo init, file commit/delete, worktree sync, push-to-DB sync |
| `app/api/git.py` (create) | Git Smart HTTP protocol endpoints (info/refs, upload-pack, receive-pack) |
| `app/services/file_service.py` (modify) | Bridge upload/delete to GitService |
| `app/api/files.py` (modify) | Accept project_id + git_path in upload |
| `app/main.py` (modify) | Register git router |

---

### Task 1: Git Config (`app/core/git_config.py`)

- [ ] **Create `backend/app/core/git_config.py`**

```python
import os
from pathlib import Path

GIT_REPO_DIR = os.getenv("GIT_REPO_DIR", str(Path(os.getenv("FILE_PATH", "./uploads")).parent / "git-repos"))
GIT_USER_NAME = "PolyPlex System"
GIT_USER_EMAIL = "system@polyplex.local"


def get_project_repo_path(project_id: int) -> Path:
    return Path(GIT_REPO_DIR, str(project_id), "repo.git")


def get_project_worktree_path(project_id: int) -> Path:
    return Path(GIT_REPO_DIR, str(project_id), "worktree")
```

### Task 2: File Model — Add `git_path` Column

- [ ] **Modify `backend/app/models/files.py`**

Add after `folder_name`:
```python
git_path = Column(String(1024), nullable=True)  # 文件在 Git 仓库中的相对路径
```

### Task 3: Git Service (`app/services/git_service.py`)

- [ ] **Create `backend/app/services/git_service.py`**

Core service with:
- `init_project_repo(project_id)` — create bare repo + initial commit
- `ensure_worktree_sync(project_id)` — checkout HEAD to worktree
- `commit_file(project_id, relative_path, content, message)` — write to worktree + commit
- `commit_delete(project_id, relative_path, message)` — delete from worktree + commit
- `sync_push_to_db(project_id, db)` — after push, scan new files into File DB
- `_git_async(*args, cwd, stdin)` — async git subprocess helper

### Task 4: Git HTTP Protocol API (`app/api/git.py`)

- [ ] **Create `backend/app/api/git.py`**

Routes:
- `GET /api/git/{repo_name}/info/refs` — advertise refs for fetch/push
- `POST /api/git/{repo_name}/git-upload-pack` — clone/fetch packfile
- `POST /api/git/{repo_name}/git-receive-pack` — receive push packfile
- Auth via JWT from Basic Auth password

### Task 5: File Service — Git Bridge

- [ ] **Modify `backend/app/services/file_service.py`**

Add Git integration to `upload_file`:
- Accept `project_id` and `git_path` parameters
- When `git_path` is set, save file to worktree and commit
- For `get_file_content`, if `git_path` is set, read from worktree

### Task 6: File API — Accept Git Parameters

- [ ] **Modify `backend/app/api/files.py`**

Update upload route to accept `project_id`, `git_path` Form params.

### Task 7: Register Git Router

- [ ] **Modify `backend/app/main.py`**

Add `from app.api.git import router as git_router` and `app.include_router(git_router)`.
