<template>
  <div class="login-page">
    <div class="login-card">
      <h1>登录</h1>
      <form @submit.prevent="handleLogin">
        <div class="field">
          <label for="username">用户名</label>
          <input id="username" v-model="form.username" type="text" placeholder="请输入用户名" required />
        </div>
        <div class="field">
          <label for="password">密码</label>
          <input id="password" v-model="form.password" type="password" placeholder="请输入密码" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :class="{ loading }" :disabled="loading">登录</button>
      </form>
      <p class="link">还没有账号？<router-link to="/form/register">去注册</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await userStore.login(form.username, form.password)
    router.push('/workbench/dashboard')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--gray-100);
}
.login-card {
  background: var(--gray-0);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  width: 380px;
}
h1 { text-align: center; margin-bottom: 24px; }
.field { margin-bottom: 16px; }
.field label { display: block; margin-bottom: 6px; font-size: 14px; color: var(--gray-700); }
.field input { width: 100%; padding: 10px 12px; border: 1px solid var(--gray-200); border-radius: 6px; font-size: 14px; box-sizing: border-box; }
.field input:focus { border-color: var(--green-deep-500); outline: none; }
.error { color: var(--red-500); font-size: 13px; margin-bottom: 12px; }
button { width: 100%; padding: 10px; background: var(--green-deep-500); color: var(--gray-0); border: none; border-radius: 6px; font-size: 15px; cursor: pointer; }
button:hover { background: var(--green-deep-600); }
button:disabled { background: var(--green-deep-200); cursor: not-allowed; }
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
@keyframes btn-spin { to { transform: rotate(360deg); } }
.link { text-align: center; margin-top: 16px; font-size: 14px; color: var(--gray-500); }
.link a { color: var(--green-deep-500); text-decoration: none; }
</style>
