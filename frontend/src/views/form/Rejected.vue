<template>
  <div class="rejected-page">
    <div class="card">
      <div class="icon-circle rejected">
        <i class="iconfont icon-ban" style="font-size:32px"></i>
      </div>
      <h2>审核未通过</h2>
      <p class="desc">
        您好 <strong>{{ userStore.username }}</strong>，您的注册申请未通过管理员审核。
      </p>

      <div v-if="reason" class="reason-box">
        <span class="reason-label">理由：</span>
        <p class="reason-text">{{ reason }}</p>
      </div>

      <!-- 申诉区域 -->
      <div class="appeal-section">
        <p class="appeal-hint">您可以修改自我介绍后重新提交审核：</p>
        <textarea
          v-model="bio"
          class="appeal-textarea"
          placeholder="请在此重新填写您的自我介绍..."
          rows="4"
        ></textarea>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
        <button
          class="appeal-btn"
          :disabled="!bio.trim() || submitting"
          @click="handleAppeal"
        >
          {{ submitting ? '提交中...' : '重新提交审核' }}
        </button>
      </div>

      <p class="hint">如有疑问，请联系管理员获取更多信息。</p>
      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import '@/assets/icon/form/iconfont.css'

const router = useRouter()
const userStore = useUserStore()
const reason = ref('')
const bio = ref('')
const errorMsg = ref('')
const submitting = ref(false)

onMounted(async () => {
  try {
    const { http } = await import('@/composables/http')
    const res = await http('/auth/user-status')
    const data = await res.json()
    reason.value = data.reason || ''
    bio.value = data.bio || ''
  } catch {
    // http 处理 401
  }
})

async function handleAppeal() {
  if (!bio.value.trim() || submitting.value) return
  submitting.value = true
  errorMsg.value = ''
  try {
    const { http } = await import('@/composables/http')
    const res = await http('/auth/reappeal', {
      method: 'POST',
      body: JSON.stringify({ bio: bio.value.trim() }),
    })
    if (!res.ok) {
      const data = await res.json()
      errorMsg.value = data.detail || '提交失败，请稍后重试'
      return
    }
    router.push('/form/pending-approval')
  } catch {
    errorMsg.value = '网络错误，请稍后重试'
  } finally {
    submitting.value = false
  }
}

function handleLogout() {
  userStore.logout()
  router.push('/home')
}
</script>

<style scoped>
.rejected-page {
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
.icon-circle.rejected { background: var(--red-50); color: var(--red-500); }
h2 { margin: 0 0 12px; font-size: 20px; color: var(--gray-900); font-weight: 600; }
.desc { color: var(--gray-500); font-size: 14px; line-height: 1.7; margin: 0 0 12px; }
.desc strong { color: var(--gray-700); }
.hint { color: var(--gray-400); font-size: 13px; margin: 0 0 24px; }

.reason-box {
  background: var(--red-50);
  border: 1px solid var(--red-100);
  border-radius: 8px;
  padding: 14px;
  margin: 0 0 16px;
  text-align: left;
}
.reason-label {
  font-size: 12px;
  color: var(--red-400);
  font-weight: 500;
}
.reason-text {
  margin: 4px 0 0;
  font-size: 14px;
  color: var(--gray-700);
  line-height: 1.6;
  white-space: pre-wrap;
}

/* 申诉区域 */
.appeal-section {
  border-top: 1px solid var(--gray-200);
  padding-top: 20px;
  margin-bottom: 16px;
}
.appeal-hint {
  font-size: 13px;
  color: var(--gray-500);
  margin: 0 0 12px;
  text-align: left;
}
.appeal-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  box-sizing: border-box;
  resize: vertical;
  color: var(--gray-900);
  transition: border-color 0.15s;
}
.appeal-textarea:focus {
  border-color: var(--green-deep-500);
  outline: none;
}
.appeal-textarea::placeholder {
  color: var(--gray-300);
}
.error-msg {
  color: var(--red-500);
  font-size: 13px;
  margin: 8px 0 0;
}
.appeal-btn {
  display: block;
  width: 100%;
  margin-top: 12px;
  padding: 10px 0;
  background: var(--green-deep-500);
  color: var(--gray-0);
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.15s;
}
.appeal-btn:hover:not(:disabled) {
  background: var(--green-deep-600);
}
.appeal-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

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
