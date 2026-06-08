const API_BASE = '/api'

/** 从 JWT token 中解析 payload（不验证签名，纯前端取 exp 用） */
function parseTokenPayload(token) {
  try {
    const parts = token.split('.')
    if (parts.length !== 3) return null
    const payload = JSON.parse(atob(parts[1]))
    return payload
  } catch {
    return null
  }
}

/** 检查 token 是否已过期（根据 exp 字段，单位秒） */
function isTokenExpired(token) {
  const payload = parseTokenPayload(token)
  if (!payload || !payload.exp) return true
  return Date.now() >= payload.exp * 1000
}

/**
 * 封装 fetch，自动附带认证头，token 过期或遇到 401 时自动登出。
 *
 * URL 为相对于 /api 的路径（如 '/auth/public-key'），
 * 会被拼接为 /api/auth/public-key。
 */
export async function http(url, options = {}) {
  const { headers, ...rest } = options

  const { useUserStore } = await import('@/stores/useUserStore')
  const userStore = useUserStore()

  // token 本地过期检查（JWT exp）
  if (userStore.token && isTokenExpired(userStore.token)) {
    userStore.logout()
    window.location.href = '/form/login'
    throw new Error('登录已过期，请重新登录')
  }

  const res = await fetch(`${API_BASE}${url}`, {
    ...rest,
    headers: {
      'Content-Type': 'application/json',
      ...(userStore.token ? { 'Authorization': `Bearer ${userStore.token}` } : {}),
      ...headers,
    },
  })

  if (res.status === 401) {
    userStore.logout()
    window.location.href = '/form/login'
    throw new Error('登录已过期，请重新登录')
  }

  return res
}

/** 安全解析 fetch 响应，非 JSON 时返回文本消息 */
export async function parseJsonSafe(res) {
  const text = await res.text()
  try {
    return JSON.parse(text)
  } catch {
    return { detail: text || `请求失败 (${res.status})` }
  }
}
