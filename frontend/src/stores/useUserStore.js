import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { JSEncrypt } from 'jsencrypt'

const API_BASE = '/api'

/** 从 JWT token payload 中检查 exp 是否已过期（前端快速判断，不验证签名） */
function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return !payload.exp || Date.now() >= payload.exp * 1000
  } catch {
    return true
  }
}

/** 安全解析 fetch 响应，非 JSON 时返回文本消息 */
async function parseJsonSafe(res) {
  const text = await res.text()
  try {
    return JSON.parse(text)
  } catch {
    return { detail: text || `请求失败 (${res.status})` }
  }
}

export const useUserStore = defineStore('user', () => {
  // 用户信息数据
  const id = ref(0)
  const _username = ref('')
  const _email = ref('')
  const _avatar = ref('')
  const token = ref('')
  const jobNumber = ref('')
  const isSystem = ref(false)

  // 其他数据
  const messageCount = ref(0)

  /** 审核状态 */
  const isApproved = ref(true) // 默认 true，兼容旧用户（不在 pending 组）

  /** 缓存的 RSA 公钥 */
  let _publicKey = null


  // 处理过后的数据
  const avatar = computed(() => {
    return _avatar.value ? `/file/compress/${_avatar.value}` : '/file/default_avatar.png'
  })
  const username = computed(() => {
    return _username.value ? _username.value : '未登录'
  })
  const email = computed(() => {
    return _email.value ? _email.value : 'none@none.com'
  })
  const hasUnreadMessage = computed(() => {
    return messageCount.value > 0
  })
  const isLoggedIn = computed(() => !!token.value)


  /**
   * 获取 RSA 公钥（缓存，只请求一次）
   */
  async function getPublicKey() {
    if (_publicKey) return _publicKey
    const res = await fetch(`${API_BASE}/auth/public-key`)
    if (!res.ok) throw new Error('无法获取加密密钥，请检查网络连接')
    const data = await res.json()
    _publicKey = data.public_key
    return _publicKey
  }

  /**
   * 用 RSA 公钥加密密码
   */
  async function encryptPassword(password) {
    try {
      const pubKey = await getPublicKey()
      const encrypt = new JSEncrypt()
      encrypt.setPublicKey(pubKey)
      const encrypted = encrypt.encrypt(password)
      if (!encrypted) throw new Error('密码加密失败')
      return encrypted
    } catch (e) {
      throw new Error(e.message || '无法连接到服务器')
    }
  }


  // 初始化：从 localStorage 恢复
  function initFromStorage() {
    const saved = localStorage.getItem('user')
    if (saved) {
      try {
        const data = JSON.parse(saved)
        // token 已过期 → 清除
        if (data.token && isTokenExpired(data.token)) {
          localStorage.removeItem('user')
          return
        }
        id.value = data.id || 0
        _username.value = data.username || ''
        _email.value = data.email || ''
        token.value = data.token || ''
        jobNumber.value = data.job_number || ''
        isSystem.value = data.is_system || false
        isApproved.value = data.is_approved !== false
      } catch {
        localStorage.removeItem('user')
      }
    }
  }

  function saveToStorage() {
    localStorage.setItem('user', JSON.stringify({
      id: id.value,
      username: _username.value,
      email: _email.value,
      token: token.value,
      job_number: jobNumber.value,
      is_system: isSystem.value,
      is_approved: isApproved.value,
    }))
  }

  function clearStorage() {
    localStorage.removeItem('user')
  }


  async function login(username, password) {
    const encrypted_password = await encryptPassword(password)

    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, encrypted_password }),
    })
    if (!res.ok) {
      const err = await parseJsonSafe(res)
      throw new Error(err.detail || '登录失败')
    }
    const data = await res.json()

    id.value = data.user.id
    _username.value = data.user.username
    _email.value = data.user.email || ''
    token.value = data.access_token
    jobNumber.value = data.user.job_number || ''
    isSystem.value = data.user.is_system || false

    saveToStorage()
    await checkApprovalStatus()
    return data
  }

  async function register(username, password, email, bio = '') {
    const encrypted_password = await encryptPassword(password)

    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, encrypted_password, email, bio }),
    })
    if (!res.ok) {
      const err = await parseJsonSafe(res)
      throw new Error(err.detail || '注册失败')
    }
    const data = await res.json()
    return data  // 返回 { message, email }，不设置登录状态
  }

  /**
   * 验证邮箱验证码，验证成功后自动登录
   */
  async function verifyCode(code) {
    const res = await fetch(`${API_BASE}/auth/verify-code`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code }),
    })
    if (!res.ok) {
      const err = await parseJsonSafe(res)
      throw new Error(err.detail || '验证失败')
    }
    const data = await res.json()

    id.value = data.user.id
    _username.value = data.user.username
    _email.value = data.user.email || ''
    token.value = data.access_token
    jobNumber.value = data.user.job_number || ''
    isSystem.value = data.user.is_system || false
    isApproved.value = false // 新注册用户处于待审核状态

    saveToStorage()
    return data
  }

  function logout() {
    id.value = 0
    _username.value = ''
    _email.value = ''
    _avatar.value = ''
    token.value = ''
    jobNumber.value = ''
    isSystem.value = false
    messageCount.value = 0
    _publicKey = null
    clearStorage()
  }

  function getAuthHeaders() {
    return {
      'Authorization': `Bearer ${token.value}`,
    }
  }

  async function checkApprovalStatus() {
    if (!token.value) {
      isApproved.value = true
      return
    }
    try {
      const { http } = await import('@/composables/http')
      const res = await http('/auth/approval-status')
      const data = await res.json()
      isApproved.value = data.status === 'approved'
    } catch {
      isApproved.value = true
    }
  }

  // 初始化
  initFromStorage()

  return {
    id,
    username,
    email,
    avatar,
    token,
    jobNumber,
    isSystem,
    messageCount,
    hasUnreadMessage,
    isLoggedIn,
    isApproved,
    login,
    register,
    verifyCode,
    logout,
    getAuthHeaders,
    checkApprovalStatus,
  }
})
