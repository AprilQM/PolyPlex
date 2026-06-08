<template>
  <div class="pending-page">
    <div class="pending-card">

      <!-- 等待审核 -->
      <template v-if="status === 'pending'">
        <div class="icon-circle pending">
          <i class="iconfont icon-clock" style="font-size:32px"></i>
        </div>
        <h2>审核中</h2>
        <p class="desc">
          您好 <strong>{{ userStore.username }}</strong>，您的账号正在等待管理员审核。
          <br><br>
          审核通过后，我们将发送邮件至 <strong>{{ userStore.email }}</strong> 通知您。
          <br><br>
          请耐心等待，谢谢。
        </p>
        <div class="poll-hint">自动检查审核状态中...</div>

        <button class="logout-btn" @click="handleLogout">退出登录</button>
      </template>

      <!-- 审核通过 -->
      <template v-else-if="status === 'approved'">
        <div class="icon-circle success">
          <i class="iconfont icon-check" style="font-size:32px"></i>
        </div>
        <h2>审核已通过</h2>
        <p class="desc">您的账号已通过审核，即将跳转至工作台...</p>
        <div class="spinner small"></div>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import '@/assets/icon/form/iconfont.css'

const router = useRouter()
const userStore = useUserStore()

const status = ref('pending')
let pollTimer = null

async function checkStatus() {
  try {
    await userStore.checkApprovalStatus()
    if (userStore.isApproved) {
      status.value = 'approved'
      clearInterval(pollTimer)
      setTimeout(() => router.push('/workbench/dashboard'), 2000)
    }
  } catch {
    // 网络错误时不做处理，下次轮询继续
  }
}

onMounted(() => {
  // 立即检查一次
  checkStatus()
  // 每 30 秒轮询
  pollTimer = setInterval(checkStatus, 30000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})

function handleLogout() {
  clearInterval(pollTimer)
  userStore.logout()
  router.push('/home')
}
</script>

<style scoped>
.pending-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--gray-100);
}
.pending-card {
  background: var(--gray-0);
  padding: 56px 48px 48px;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  width: 440px;
  text-align: center;
  position: relative;
  overflow: hidden;
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
.icon-circle.pending { background: var(--yellow-50); color: var(--yellow-500); }
.icon-circle.success { background: var(--green-50); color: var(--green-500); }

h2 { margin: 0 0 12px; font-size: 20px; color: var(--gray-900); font-weight: 600; }
.desc { color: var(--gray-500); font-size: 14px; line-height: 1.7; margin: 0 0 24px; }
.desc strong { color: var(--gray-700); }

.poll-hint {
  color: var(--gray-400);
  font-size: 13px;
  margin-bottom: 12px;
}

.spinner {
  width: 36px; height: 36px;
  border: 3px solid var(--gray-200);
  border-top-color: var(--green-deep-500);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}
.spinner.small { width: 20px; height: 20px; border-width: 2px; }
@keyframes spin { to { transform: rotate(360deg); } }

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
