"""
邮件发送模块 — SMTP + HTML 模板
"""
import os
import time
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.qq.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_SENDER = os.getenv("SMTP_SENDER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5173")

# ── 品牌色 ──
GREEN_DEEP = "#1a4d3e"
PEACH = "#e2906f"
BLUE = "#3b82f6"
GRAY_50 = "#f9fafb"
GRAY_200 = "#e5e7eb"
GRAY_500 = "#6b7280"
GRAY_700 = "#374151"
GRAY_900 = "#111827"

EMAIL_TEMPLATE = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:{GRAY_50};font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;">
<table width="100%%" cellpadding="0" cellspacing="0" style="background:{GRAY_50};padding:40px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
<tr><td style="background:{GREEN_DEEP};padding:32px 40px;text-align:center;">
<h1 style="color:#fff;margin:0;font-size:22px;font-weight:600;">{{title}}</h1>
</td></tr>
<tr><td style="padding:40px;">
<p style="color:{GRAY_700};font-size:15px;line-height:1.7;margin:0 0 20px;">{{content}}</p>
{{verify_button}}
</td></tr>
<tr><td style="background:{GRAY_50};padding:20px 40px;text-align:center;border-top:1px solid {GRAY_200};">
<p style="color:{GRAY_500};font-size:12px;margin:0;">PolyPlex &copy; {{time_year}} &middot; 让每一个创意都有生长的土壤</p>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""


def _build_verify_button(url: str) -> str:
    return f'''
<table cellpadding="0" cellspacing="0" style="margin:24px auto;">
<tr><td align="center" style="background:{BLUE};border-radius:8px;padding:0;">
<a href="{url}" target="_blank" style="display:inline-block;padding:12px 36px;color:#fff;text-decoration:none;font-size:15px;font-weight:500;border-radius:8px;">验证邮箱</a>
</td></tr>
</table>
<p style="color:{GRAY_500};font-size:13px;text-align:center;margin:12px 0 0;">或复制链接到浏览器访问：<br><span style="color:{GRAY_500};word-break:break-all;">{url}</span></p>'''


def _build_login_button(url: str) -> str:
    return f'''
<table cellpadding="0" cellspacing="0" style="margin:24px auto;">
<tr><td align="center" style="background:{GREEN_DEEP};border-radius:8px;padding:0;">
<a href="{url}" target="_blank" style="display:inline-block;padding:12px 36px;color:#fff;text-decoration:none;font-size:15px;font-weight:500;border-radius:8px;">登录 PolyPlex</a>
</td></tr>
</table>
<p style="color:{GRAY_500};font-size:13px;text-align:center;margin:12px 0 0;">或复制链接到浏览器访问：<br><span style="color:{GRAY_500};word-break:break-all;">{url}</span></p>'''


async def send_approval_email(receiver: str, username: str) -> bool:
    """发送审核通过通知邮件"""
    login_url = f"{APP_BASE_URL}/form/login"
    title = "审核通过通知"
    content = f"您好 {username}，<br><br>恭喜您！您的 PolyPlex 账号已通过管理员审核。<br><br>现在您可以登录系统，开始使用所有功能：<br>创建项目、邀请团队成员、探索灵感、协作创作。<br><br>欢迎加入 PolyPlex！"
    login_button = _build_login_button(login_url)

    return await _send(receiver, title, content, login_button)


async def send_rejection_email(receiver: str, username: str, reason: str, bio: str = "") -> bool:
    """发送审核拒绝通知邮件（含理由和自我介绍）"""
    title = "审核未通过"
    escaped_reason = reason.replace("\n", "<br>")
    escaped_bio = bio.replace("\n", "<br>") if bio else ""
    content = f"您好 {username}，<br><br>很遗憾，您的 PolyPlex 账号申请未通过管理员审核。"
    if escaped_bio:
        content += f"<br><br>您提交的自我介绍：<br><span style=\"color:#6b7280;font-style:italic;\">{escaped_bio}</span>"
    content += f"<br><br>拒绝原因：<br><span style=\"color:#6b7280;font-style:italic;\">{escaped_reason}</span><br><br>如有疑问，请联系管理员获取更多信息。"
    return await _send(receiver, title, content)


async def send_verify_email(receiver: str, code: str, username: str) -> bool:
    """发送邮箱验证邮件"""
    verify_url = f"{APP_BASE_URL}/form/verify?code={code}"
    title = "验证您的邮箱地址"
    content = f"您好 {username}，<br><br>您正在注册 PolyPlex 账号，请点击下方按钮验证您的邮箱：<br><br>邮箱：{receiver}<br>有效期：30 分钟"
    verify_button = _build_verify_button(verify_url)

    return await _send(receiver, title, content, verify_button)


async def _send(receiver: str, title: str, content: str, verify_button: str = "") -> bool:
    """底层 SMTP 发送（异步，在线程池执行）"""
    msg = MIMEMultipart()
    msg["From"] = SMTP_SENDER
    msg["To"] = receiver
    msg["Subject"] = f"【PolyPlex】{title}"

    html = EMAIL_TEMPLATE.replace("{title}", title) \
        .replace("{content}", content) \
        .replace("{verify_button}", verify_button) \
        .replace("{time_year}", str(time.localtime().tm_year))

    msg.attach(MIMEText(html, "html", "utf-8"))

    return await asyncio.to_thread(_smtp_send, msg, receiver)


def _smtp_send(msg: MIMEMultipart, receiver: str) -> bool:
    """同步 SMTP 发送（在 asyncio.to_thread 中执行）"""
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_SENDER, SMTP_PASSWORD)
        server.sendmail(SMTP_SENDER, receiver, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False
