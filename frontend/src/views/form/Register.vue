<template>
  <div class="register-page">
    <div class="register-card">
      <h1>注册</h1>

      <!-- 注册表单 -->
      <form v-if="!emailSent" @submit.prevent="handleRegister">
        <div class="field">
          <label for="email">邮箱</label>
          <input id="email" v-model="form.email" type="email" placeholder="请输入邮箱" required />
        </div>
        <div class="field">
          <label for="username">用户名</label>
          <input id="username" v-model="form.username" type="text" placeholder="请输入用户名" required />
        </div>
        <div class="field">
          <label for="password">密码</label>
          <input id="password" v-model="form.password" type="password" placeholder="请输入密码" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :class="{ loading }" :disabled="loading">注册</button>
      </form>

      <!-- 邮件已发送提示 -->
      <div v-else class="email-sent">
        <div class="icon">&#9993;</div>
        <h2>验证邮件已发送</h2>
        <p>我们已向 <strong>{{ registeredEmail }}</strong> 发送了一封验证邮件，请点击邮件中的链接完成注册。</p>
        <p class="hint">有效期 30 分钟，如未收到请检查垃圾邮件</p>
        <button class="secondary" :class="{ loading: resending }" @click="resend" :disabled="resending">
          重新发送邮件
        </button>
      </div>

      <p class="link">已有账号？<router-link to="/form/login">去登录</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({ username: '', password: '', email: '' })
const loading = ref(false)
const error = ref('')
const emailSent = ref(false)
const registeredEmail = ref('')
const resending = ref(false)

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    const result = await userStore.register(
      form.username,
      form.password,
      form.email,
    )
    registeredEmail.value = form.email
    emailSent.value = true
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function resend() {
  resending.value = true
  error.value = ''
  try {
    const res = await fetch('/api/auth/register/resend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: registeredEmail.value }),
    })
    if (!res.ok) {
      const text = await res.text()
      let detail = '重新发送失败'
      try { detail = JSON.parse(text).detail || detail } catch {}
      throw new Error(detail)
    }
  } catch (e) {
    error.value = e.message
  } finally {
    resending.value = false
  }
}
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--gray-100);
}
.register-card {
  background: var(--gray-0);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  width: 380px;
}
h1 { text-align: center; margin-bottom: 24px; }
h2 { text-align: center; margin: 16px 0 12px; font-size: 18px; color: var(--green-deep-500); }
.field { margin-bottom: 16px; }
.field label { display: block; margin-bottom: 6px; font-size: 14px; color: var(--gray-700); }
.field input { width: 100%; padding: 10px 12px; border: 1px solid var(--gray-200); border-radius: 6px; font-size: 14px; box-sizing: border-box; }
.field input:focus { border-color: var(--green-deep-500); outline: none; }
.error { color: var(--red-500); font-size: 13px; margin-bottom: 12px; }
button { width: 100%; padding: 10px; background: var(--green-deep-500); color: var(--gray-0); border: none; border-radius: 6px; font-size: 15px; cursor: pointer; }
button:hover { background: var(--green-deep-600); }
button:disabled { background: var(--green-deep-200); cursor: not-allowed; }
button.secondary { background: var(--gray-0); color: var(--green-deep-500); border: 1px solid var(--green-deep-500); margin-top: 12px; }
button.secondary:hover { background: var(--green-deep-50); }
button.loading { position: relative; color: transparent; }
button.loading::after {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 20px; height: 20px;
  margin-top: -10px;
  margin-left: -10px;
  border: 3px solid rgba(255,255,255,0.3);
  border-top-color: var(--gray-0);
  border-radius: 50%;
  animation: btn-spin 0.7s linear infinite;
}
button.secondary.loading::after {
  border-color: var(--green-deep-200);
  border-top-color: var(--green-deep-500);
}
@keyframes btn-spin { to { transform: rotate(360deg); } }
.link { text-align: center; margin-top: 16px; font-size: 14px; color: var(--gray-500); }
.link a { color: var(--green-deep-500); text-decoration: none; }
.email-sent { text-align: center; }
.email-sent .icon { font-size: 48px; color: var(--green-500); }
.email-sent p { font-size: 14px; color: var(--gray-600); line-height: 1.6; }
.email-sent .hint { font-size: 12px; color: var(--gray-400); }
</style>
