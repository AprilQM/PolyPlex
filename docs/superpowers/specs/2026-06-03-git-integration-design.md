# Git Integration Design

> **Goal:** Make PolyPlex a Git server that standard Git clients can clone/push/pull from via HTTP, with file management as the underlying storage layer.

**Architecture:** Each project gets a bare Git repository for Git protocol operations. The Git working tree serves as the physical storage for project files — file uploads write to the working tree and commit to the bare repo; Git pushes update the bare repo and sync back to the file database. The file management system (File model, CRUD, API) is the authoritative data source; the bare repo is the Git protocol interface.

**Tech Stack:** FastAPI (Python) + Git subprocess + MySQL (asyncmy) + Vue 3

---

## Design Decisions

### Git Bare Repo + Working Tree = File Storage

The Git working tree IS the physical storage for project files:
- File upload (web UI) → write to working tree → git commit → bare repo
- Git push → bare repo → checkout to working tree → register in File DB
- File download → read from working tree (via existing file API)

### No UUID Folder for Project Files

Project files are stored in the Git working tree at `{GIT_REPO_DIR}/{project_id}/worktree/`. The UUID-based storage is no longer used for project-managed files (avatars and system files may still use it).

### File DB Is the Source of Truth

The File model tracks all file metadata (UUID, hash, size, path, uploader). On Git push, changes are scanned and the File DB is updated. On web upload, the File DB is updated first, then the Git repo.

---

## Components

### 1. Git Config (`app/core/git_config.py`)
- `GIT_REPO_DIR` - where bare repos and worktrees live
- `GIT_USER_NAME` / `GIT_USER_EMAIL` - author info for automated commits
- `ProjectGitRepo` dataclass with repo/worktree paths

### 2. Git Service (`app/services/git_service.py`)
- `init_project_repo(project_id)` — create bare repo with initial commit
- `init_worktree(project_id)` — checkout bare repo HEAD to worktree
- `ensure_worktree_sync(project_id)` — ensure worktree matches HEAD
- `commit_file(project_id, relative_path, content, message)` — write file to worktree, stage, commit, push to bare
- `commit_delete(project_id, relative_path, message)` — delete file from worktree, commit
- `sync_push_to_db(project_id, db_session)` — after push, extract new/changed files from repo, register in File DB
- `delete_project_repo(project_id)` — remove repo and worktree
- Internal helpers: `_git()`, `_git_pipe()` for subprocess calls

### 3. Git HTTP Protocol API (`app/api/git.py`)
- `GET /api/git/{repo_name}/info/refs` — advertise refs for fetch/push
- `POST /api/git/{repo_name}/git-upload-pack` — serve pack data (clone/fetch)
- `POST /api/git/{repo_name}/git-receive-pack` — receive pack data (push)
- Auth via Bearer token in `Authorization` header (or Basic Auth)

### 4. File Model Changes (`app/models/files.py`)
- Add `git_path VARCHAR(1024)` field — relative path in the Git repo
- Add `project_id BIGINT` FK if not already present

### 5. File Service Changes (`app/services/file_service.py`)
- After file upload: if target is a project, call `git_service.commit_file()`
- After file delete: if git_path exists, call `git_service.commit_delete()`

### 6. File API Changes (`app/api/files.py`)
- Upload route: accept `project_id` + `git_path` parameters
- After push sync: after `git-receive-pack`, trigger `sync_push_to_db()`

---

## Git HTTP Protocol Flow

### Clone/Fetch (Read)
```
Client: GET /api/git/{repo}/info/refs?service=git-upload-pack
Server: git upload-pack --advertise-refs {bare_repo_path}
        → returns refs and capabilities

Client: POST /api/git/{repo}/git-upload-pack
  Body: wants + haves in pkt-line format
Server: git upload-pack --stateless-rpc {bare_repo_path} < stdin
        → returns packfile
```

### Push (Write)
```
Client: GET /api/git/{repo}/info/refs?service=git-receive-pack
Server: git receive-pack --advertise-refs {bare_repo_path}
        → returns refs and capabilities

Client: POST /api/git/{repo}/git-receive-pack
  Body: commands + packfile in pkt-line format
Server: git receive-pack --stateless-rpc {bare_repo_path} < stdin
        → updates refs

After push → sync_push_to_db(): 
  - Compare old/new HEAD
  - List changed files
  - Register new files in File DB
  - Checkout HEAD to worktree
```

---

## Frontend

Minimal frontend additions:
- Project settings page: show Git remote URL (`http://{host}/api/git/{project_name}.git`)
- Token copy button for Git authentication

---

## Directory Layout

```
{GIT_REPO_DIR}/
  {project_id}/
    repo.git/       ← bare repository
    worktree/       ← working tree (file storage)
      src/
      docs/
      assets/
      ...
```

## Auth Flow for Git

Git HTTP supports Basic Auth. PolyPlex uses Bearer tokens. Flow:
1. Client: `git clone http://polyplex/api/git/project.git`
2. Git prompts for username/password → user enters token as password
3. Server validates Bearer token from Basic Auth password field
4. Checks user has access to the project via ProjectMember table
5. If authorized, proceed with Git operation; if not, return 401

## Implementation Order

1. Git config + Git service (repo init, worktree management)
2. Git HTTP protocol endpoints (info/refs, upload-pack, receive-pack)
3. File model changes (git_path, project_id)
4. File service bridge (upload → commit)
5. Push sync (push → DB registration)
6. Frontend (Git URL display)
