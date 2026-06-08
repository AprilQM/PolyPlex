"""
PolyPlex 认证流程测试 — 纯前端模拟

和前端一样调用 API，验证码从邮件获取后手动输入。
支持自动测试 JWT 认证对 files / groups 接口的保护。

用法:
  # 先启动后端
  python backend/main.py

  # 手动交互测试（注册/登录需要查邮件验证码）
  python tests/test_auth_flow.py

  # 自动测试（需要已启动的服务 + 数据库中有测试用户）
  python tests/test_auth_flow.py --auto
"""
import sys
import base64
import argparse

import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

API_BASE = "http://127.0.0.1:8000/api"


# ── RSA 加密 ──

def get_public_key() -> str:
    r = requests.get(f"{API_BASE}/auth/public-key")
    r.raise_for_status()
    return r.json()["public_key"]


def rsa_encrypt(password: str, public_key_pem: str) -> str:
    key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    encrypted = key.encrypt(
        password.encode("utf-8"),
        padding.PKCS1v15(),
    )
    return base64.b64encode(encrypted).decode("utf-8")


# ── Auth API ──

def api_register(username: str, email: str, encrypted_password: str) -> dict:
    r = requests.post(f"{API_BASE}/auth/register", json={
        "username": username,
        "encrypted_password": encrypted_password,
        "email": email,
    })
    if r.status_code != 200:
        raise RuntimeError(r.json().get("detail", r.text))
    return r.json()


def api_verify_code(code: str) -> dict:
    r = requests.post(f"{API_BASE}/auth/verify-code", json={"code": code})
    if r.status_code != 200:
        raise RuntimeError(r.json().get("detail", r.text))
    return r.json()


def api_login(username: str, encrypted_password: str) -> dict:
    r = requests.post(f"{API_BASE}/auth/login", json={
        "username": username,
        "encrypted_password": encrypted_password,
    })
    if r.status_code != 200:
        raise RuntimeError(r.json().get("detail", r.text))
    return r.json()


def api_me(token: str) -> dict:
    r = requests.get(f"{API_BASE}/auth/me", headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return r.json()["user"]


# ── 注册流程（手动） ──

def register_flow():
    print("\n── 注册新账号 ──")
    username = input("  用户名: ").strip()
    email = input("  邮箱: ").strip()
    password = input("  密码: ").strip()

    print("\n  获取 RSA 公钥...")
    pubkey = get_public_key()
    encrypted_password = rsa_encrypt(password, pubkey)

    print("  发送注册请求...")
    try:
        result = api_register(username, email, encrypted_password)
    except RuntimeError as e:
        print(f"  ! 注册失败: {e}")
        return
    print(f"  ✓ 验证邮件已发送至 {result['email']}")

    print("\n  请查看邮箱，获取验证链接中的 code 参数")
    print("  (链接格式: http://.../form/verify?code=xxxxxxxx)")
    code = input("  验证码: ").strip()
    if not code:
        print("  ! 未输入验证码，跳过")
        return

    print("  验证邮箱...")
    try:
        result = api_verify_code(code)
    except RuntimeError as e:
        print(f"  ! 验证失败: {e}")
        return

    token = result["access_token"]
    user = result["user"]
    print(f"  ✓ 验证成功！用户 {user['username']} 已创建并自动登录")
    print(f"  Token: {token[:60]}...")

    print("\n  验证 /api/auth/me ...")
    me = api_me(token)
    assert me["username"] == username
    assert me["email"] == email
    print(f"  ✓ 当前用户: {me['username']} / {me['email']} / ID: {me['id']}")

    print("\n  [OK] 注册 + 邮箱验证全流程通过！")


def login_flow():
    print("\n── 登录已有账号 ──")
    username = input("  用户名: ").strip()
    password = input("  密码: ").strip()

    print("\n  获取 RSA 公钥...")
    pubkey = get_public_key()
    encrypted_password = rsa_encrypt(password, pubkey)

    print("  发送登录请求...")
    try:
        result = api_login(username, encrypted_password)
    except RuntimeError as e:
        print(f"  ! 登录失败: {e}")
        return

    token = result["access_token"]
    user = result["user"]
    print(f"  ✓ 登录成功！用户: {user['username']} / {user.get('email', '')}")
    print(f"  Token: {token[:60]}...")

    print("\n  验证 /api/auth/me ...")
    me = api_me(token)
    assert me["username"] == username
    print(f"  ✓ 当前用户: {me['username']} / {me['email']} / ID: {me['id']}")

    print("\n  [OK] 登录验证通过！")


# ── 自动测试：JWT 认证保护 ──

def auto_test_jwt_required():
    """
    测试 files / groups 接口是否正确拒绝未认证请求。
    需要服务器已启动，且 /api/auth/login 可用。
    """
    print("\n── 检测 JWT 认证保护 ──")

    # 1. 无 token 请求文件列表 → 应 403（bearer_scheme auto_error=False → 走 require 逻辑）
    r = requests.get(f"{API_BASE}/files", headers={})
    assert r.status_code in (401, 403), f"GET /api/files 未认证应返回 401/403，实际 {r.status_code}"
    print("  ✓ GET /api/files 无 token → 被拦截")

    # 2. 无 token 请求上传 → 应 401/403
    r = requests.post(f"{API_BASE}/files/upload", headers={})
    assert r.status_code in (401, 403), f"POST /api/files/upload 未认证应返回 401/403，实际 {r.status_code}"
    print("  ✓ POST /api/files/upload 无 token → 被拦截")

    # 3. 无 token 请求文件下载
    r = requests.get(f"{API_BASE}/files/some-uuid/download", headers={})
    assert r.status_code in (401, 403), f"GET /api/files/.../download 未认证应返回 401/403，实际 {r.status_code}"
    print("  ✓ GET /api/files/*/download 无 token → 被拦截")

    # 4. 无 token 请求组列表
    r = requests.get(f"{API_BASE}/groups", headers={})
    assert r.status_code in (401, 403), f"GET /api/groups 未认证应返回 401/403，实际 {r.status_code}"
    print("  ✓ GET /api/groups 无 token → 被拦截")

    # 5. 无 token 创建组
    r = requests.post(f"{API_BASE}/groups", headers={})
    assert r.status_code in (401, 403), f"POST /api/groups 未认证应返回 401/403，实际 {r.status_code}"
    print("  ✓ POST /api/groups 无 token → 被拦截")

    # 6. 有效 token 应正常
    pubkey = get_public_key()
    username = input("  输入已有账号的用户名: ").strip()
    password = input("  输入密码: ").strip()
    encrypted_password = rsa_encrypt(password, pubkey)
    try:
        login_result = api_login(username, encrypted_password)
    except RuntimeError as e:
        print(f"  ! 登录失败: {e}")
        print("  ⚠ 跳过 token 有效性测试")
        return
    token = login_result["access_token"]

    # 用有效 token 请求文件列表
    r = requests.get(f"{API_BASE}/files", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, f"有 token 的 GET /api/files 应返回 200，实际 {r.status_code}"
    print("  ✓ GET /api/files 有 token → 200")

    # 用有效 token 请求组列表
    r = requests.get(f"{API_BASE}/groups", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, f"有 token 的 GET /api/groups 应返回 200，实际 {r.status_code}"
    print("  ✓ GET /api/groups 有 token → 200")

    print("  [OK] JWT 认证保护全部通过！")


# ── 入口 ──

def main():
    parser = argparse.ArgumentParser(description="PolyPlex 认证测试")
    parser.add_argument("--auto", action="store_true", help="运行自动测试（跳过手动交互）")
    args = parser.parse_args()

    if args.auto:
        auto_test_jwt_required()
        return

    print("=" * 50)
    print("PolyPlex 认证测试（纯前端模拟）")
    print("=" * 50)
    print("1. 注册新账号")
    print("2. 登录已有账号")
    print("3. 自动测试 JWT 认证保护")
    choice = input("\n请选择 (1/2/3): ").strip()

    if choice == "3":
        auto_test_jwt_required()
    elif choice == "1":
        register_flow()
    else:
        login_flow()

    print("=" * 50)


if __name__ == "__main__":
    main()
