"""
Git 集成服务 — 管理代码仓库组件的 Git 仓库

职责：
- 初始化/删除 Git 仓库（bare repo + worktree）
- 文件写入/删除时自动 commit
- Git push 后将文件同步到 File DB

每个 Git 仓库对应一个 GitRepoComponent 实例，repo_id = 组件的 Snowflake ID。
"""
import os
import asyncio
import hashlib
import mimetypes
import shutil
from pathlib import Path
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.git_config import (
    get_repo_path,
    get_worktree_path,
    ensure_git_dirs,
    GIT_USER_NAME,
    GIT_USER_EMAIL,
)


class GitService:
    """管理 Git 仓库"""

    GIT_TIMEOUT = 120  # git 命令超时（秒）

    # ── 底层 git 命令执行 ──────────────────────────────────────────

    @staticmethod
    async def _git_async(
        *args: str,
        cwd: Optional[Path] = None,
        stdin: Optional[bytes] = None,
        env: Optional[dict] = None,
    ) -> tuple[int, bytes, bytes]:
        """异步执行 git 命令"""
        cmd = ["git"] + list(args)
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(cwd) if cwd else None,
            stdin=asyncio.subprocess.PIPE if stdin is not None else None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=stdin),
                timeout=GitService.GIT_TIMEOUT,
            )
            return proc.returncode or 0, stdout, stderr
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return -1, b"", b"Timeout"

    # ── 仓库初始化 ─────────────────────────────────────────────────

    @classmethod
    async def init_repo(cls, repo_id: int):
        """初始化 Git 仓库

        创建 bare repo → 初始化 worktree → 首次 commit → 推送到 bare
        repo_id 是 GitRepoComponent 实例的 Snowflake ID
        """
        repo_path = get_repo_path(repo_id)
        if repo_path.exists():
            return  # 已存在

        repo_path.parent.mkdir(parents=True, exist_ok=True)

        # 1) 创建 bare repo
        rc, _, err = await cls._git_async("init", "--bare", str(repo_path))
        if rc != 0:
            raise RuntimeError(f"创建 bare repo 失败: {err.decode()}")

        # 2) 启用 receive-pack（允许 push）
        await cls._git_async("config", "http.receivepack", "true", cwd=repo_path)

        # 3) 初始化 worktree 并创建初始 commit
        worktree_path = get_worktree_path(repo_id)
        worktree_path.mkdir(parents=True, exist_ok=True)

        rc, _, err = await cls._git_async("init", cwd=worktree_path)
        if rc != 0:
            raise RuntimeError(f"初始化 worktree 失败: {err.decode()}")

        # 设置 git 用户
        await cls._git_async("config", "user.name", GIT_USER_NAME, cwd=worktree_path)
        await cls._git_async("config", "user.email", GIT_USER_EMAIL, cwd=worktree_path)

        # 创建 .gitkeep 确保有初始提交
        keep_file = worktree_path / ".gitkeep"
        keep_file.write_text("")

        await cls._git_async("add", ".gitkeep", cwd=worktree_path)
        rc, _, err = await cls._git_async(
            "-c", f"user.name={GIT_USER_NAME}",
            "-c", f"user.email={GIT_USER_EMAIL}",
            "commit", "-m", "Initial commit",
            cwd=worktree_path,
        )
        if rc != 0:
            raise RuntimeError(f"创建初始 commit 失败: {err.decode()}")

        # 4) 添加 remote 并推送
        await cls._git_async(
            "remote", "add", "origin", str(repo_path),
            cwd=worktree_path,
        )
        rc, _, err = await cls._git_async(
            "push", "-u", "origin", "master",
            cwd=worktree_path,
        )
        if rc != 0:
            raise RuntimeError(f"推送初始 commit 失败: {err.decode()}")

    # ── 工作树同步 ─────────────────────────────────────────────────

    @classmethod
    async def ensure_worktree_sync(cls, repo_id: int):
        """确保 worktree 与 bare repo HEAD 一致"""
        repo_path = get_repo_path(repo_id)
        worktree_path = get_worktree_path(repo_id)

        if not repo_path.exists():
            await cls.init_repo(repo_id)
            return

        if not (worktree_path / ".git").exists():
            shutil.rmtree(worktree_path, ignore_errors=True)
            worktree_path.mkdir(parents=True, exist_ok=True)
            rc, _, err = await cls._git_async(
                "clone", str(repo_path), str(worktree_path),
            )
            if rc != 0:
                await cls.init_repo(repo_id)
                return

        # 拉取最新并强制 checkout
        await cls._git_async("fetch", "origin", cwd=worktree_path)
        await cls._git_async("checkout", "master", "--force", cwd=worktree_path)
        await cls._git_async("reset", "--hard", "origin/master", cwd=worktree_path)

        # 确保 git 用户配置
        await cls._git_async("config", "user.name", GIT_USER_NAME, cwd=worktree_path)
        await cls._git_async("config", "user.email", GIT_USER_EMAIL, cwd=worktree_path)

    # ── 文件操作 ───────────────────────────────────────────────────

    @classmethod
    async def commit_file(
        cls,
        repo_id: int,
        relative_path: str,
        content: bytes,
        message: str,
    ):
        """将文件写入 worktree 并 commit

        Args:
            repo_id: GitRepoComponent 实例的 Snowflake ID
            relative_path: 仓库内相对路径，如 "src/main.py"
            content: 文件内容（bytes）
            message: commit message
        """
        worktree_path = get_worktree_path(repo_id)
        if not worktree_path.exists():
            await cls.init_repo(repo_id)

        file_path = worktree_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入文件
        file_path.write_bytes(content)

        # git add + commit + push
        await cls._git_async("add", relative_path, cwd=worktree_path)
        rc, _, err = await cls._git_async(
            "-c", f"user.name={GIT_USER_NAME}",
            "-c", f"user.email={GIT_USER_EMAIL}",
            "commit", "-m", message,
            cwd=worktree_path,
        )
        if rc == 0:
            await cls._git_async("push", "origin", "master", cwd=worktree_path)

    @classmethod
    async def commit_delete(
        cls,
        repo_id: int,
        relative_path: str,
        message: str,
    ):
        """从 worktree 删除文件并 commit"""
        worktree_path = get_worktree_path(repo_id)
        file_path = worktree_path / relative_path

        if not file_path.exists():
            return

        await cls._git_async("rm", relative_path, cwd=worktree_path)
        rc, _, err = await cls._git_async(
            "-c", f"user.name={GIT_USER_NAME}",
            "-c", f"user.email={GIT_USER_EMAIL}",
            "commit", "-m", message,
            cwd=worktree_path,
        )
        if rc == 0:
            await cls._git_async("push", "origin", "master", cwd=worktree_path)

    # ── Push 后同步到 File DB ─────────────────────────────────────

    @classmethod
    async def sync_push_to_db(cls, repo_id: int, db: AsyncSession, uploader_id: int = 0):
        """Git push 后，扫描新文件并注册到 File DB

        在 git-receive-pack 完成后调用。遍历 worktree 中不在 DB 的文件，
        自动注册到文件数据库。
        """
        await cls.ensure_worktree_sync(repo_id)

        worktree_path = get_worktree_path(repo_id)
        if not worktree_path.exists():
            return

        from app.crud.files import get_file_by_hash, create_file

        for file_path in sorted(worktree_path.rglob("*")):
            if not file_path.is_file():
                continue
            if file_path.name in (".gitkeep", ".DS_Store"):
                continue
            if ".git" in file_path.parts:
                continue

            relative = str(file_path.relative_to(worktree_path)).replace("\\", "/")

            # 计算哈希
            content = file_path.read_bytes()
            file_hash = hashlib.sha256(content).hexdigest()

            # 检查是否已存在
            existing = await get_file_by_hash(db, file_hash)
            if existing:
                continue

            # 注册到 DB
            ext = file_path.suffix.lower()
            mime_type, _ = mimetypes.guess_type(str(file_path))
            folder_name = f"git:{repo_id}"

            await create_file(
                db=db,
                filename=file_path.name,
                file_size=len(content),
                file_type=mime_type or "application/octet-stream",
                file_ext=ext,
                folder_name=folder_name,
                uploader_id=uploader_id,
                file_hash=file_hash,
                target_type="component",
                target_id=repo_id,
            )

    # ── 删除仓库 ───────────────────────────────────────────────────

    @staticmethod
    def delete_repo(repo_id: int):
        """删除 Git 仓库"""
        repo_path = get_repo_path(repo_id)
        worktree_path = get_worktree_path(repo_id)

        if repo_path.exists():
            shutil.rmtree(repo_path)
        if worktree_path.exists():
            shutil.rmtree(worktree_path)
