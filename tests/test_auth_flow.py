"""
PolyPlex 认证流程测试 — 纯前端模拟
和前端一样调用 API，验证码从邮件获取后手动输入。

用法:
  conda activate polyplex
  python tests/test_auth_flow.py
"""
import sys
import base64

import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

API_BASE = "http://127.0.0.1:8000/api/auth"


# ── RSA 加密 ──

def get_public_key() -> str:
    r = requests.get(f"{API_BASE}/public-key")
    r.raise_for_status()
    return r.json()["public_key"]


def rsa_encrypt(password: str, public_key_pem: str) -> str:
    key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    encrypted = key.encrypt(
        password.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return base64.b64encode(encrypted).decode("utf-8")


# ── API ──

def api_register(username: str, email: str, encrypted_password: str) -> dict:
    r = requests.post(f"{API_BASE}/register", json={
        "username": username,
        "encrypted_password": encrypted_password,
        "email": email,
    })
    if r.status_code != 200:
        raise RuntimeError(r.json().get("detail", r.text))
    return r.json()


def api_verify_code(code: str) -> dict:
    r = requests.post(f"{API_BASE}/verify-code", json={"code": code})
    if r.status_code != 200:
        raise RuntimeError(r.json().get("detail", r.text))
    return r.json()


def api_login(username: str, encrypted_password: str) -> dict:
    r = requests.post(f"{API_BASE}/login", json={
        "username": username,
        "encrypted_password": encrypted_password,
    })
    if r.status_code != 200:
        raise RuntimeError(r.json().get("detail", r.text))
    return r.json()


def api_me(token: str) -> dict:
    r = requests.get(f"{API_BASE}/me", headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return r.json()["user"]


# ── 流程 ──

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

    # 等待用户从邮件获取验证码
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

    # 验证 /me
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


# ── 入口 ──

def main():
    print("=" * 50)
    print("PolyPlex 认证测试（纯前端模拟）")
    print("=" * 50)
    print("1. 注册新账号")
    print("2. 登录已有账号")
    choice = input("\n请选择 (1/2): ").strip()

    if choice == "1":
        register_flow()
    else:
        login_flow()

    print("=" * 50)


if __name__ == "__main__":
    main()
