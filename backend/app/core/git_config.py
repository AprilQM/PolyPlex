"""Git 集成配置"""
import os
from pathlib import Path

# Git 仓库存储根目录（每个组件仓库一个子目录）
GIT_REPO_DIR = os.getenv(
    "GIT_REPO_DIR",
    str(Path(os.getenv("FILE_PATH", "./uploads")).parent / "git-repos"),
)

# Git 自动提交的作者信息
GIT_USER_NAME = "PolyPlex System"
GIT_USER_EMAIL = "system@polyplex.local"


def get_repo_path(repo_id: int) -> Path:
    """获取 repo 的 bare repo 路径

    repo_id 是 GitRepoComponent 实例的 Snowflake ID
    """
    return Path(GIT_REPO_DIR, str(repo_id), "repo.git")


def get_worktree_path(repo_id: int) -> Path:
    """获取 repo 的工作树路径（文件实际存储位置）"""
    return Path(GIT_REPO_DIR, str(repo_id), "worktree")


def ensure_git_dirs(repo_id: int):
    """确保 Git 目录结构存在"""
    repo_path = get_repo_path(repo_id)
    worktree_path = get_worktree_path(repo_id)
    repo_path.parent.mkdir(parents=True, exist_ok=True)
    worktree_path.mkdir(parents=True, exist_ok=True)
    return repo_path, worktree_path
