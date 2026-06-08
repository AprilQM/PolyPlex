<template>
  <div class="banned-page">
    <div class="card">
      <div class="icon-circle banned">
        <i class="iconfont icon-ban" style="font-size:32px"></i>
      </div>
      <h2>账号已被封禁</h2>
      <p class="desc">
        您好 <strong>{{ userStore.username }}</strong>，您的账号已被封禁，无法访问平台功能。
      </p>
      <p class="hint">如有疑问，请联系管理员。</p>
      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import '@/assets/icon/form/iconfont.css'

const router = useRouter()
const userStore = useUserStore()

function handleLogout() {
  userStore.logout()
  router.push('/home')
}
</script>

<style scoped>
.banned-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--gray-100);
}
.card {
  background: var(--gray-0);
  padding: 56px 48px 48px;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  width: 440px;
  text-align: center;
}
.icon-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}
.icon-circle.banned { background: var(--red-50); color: var(--red-500); }
h2 { margin: 0 0 12px; font-size: 20px; color: var(--gray-900); font-weight: 600; }
.desc { color: var(--gray-500); font-size: 14px; line-height: 1.7; margin: 0 0 12px; }
.desc strong { color: var(--gray-700); }
.hint { color: var(--gray-400); font-size: 13px; margin: 0 0 24px; }

.logout-btn {
  padding: 10px 32px;
  background: var(--gray-0);
  color: var(--gray-500);
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}
.logout-btn:hover {
  color: var(--red-500);
  border-color: var(--red-200);
  background: var(--red-50);
}
</style>
