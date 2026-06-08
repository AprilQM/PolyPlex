<template>
  <div class="pending-users">
    <h1 class="page-title">用户审核</h1>

    <div v-if="loading" class="loading-state">加载中...</div>

    <template v-else-if="items.length === 0">
      <div class="empty-state">
        <i class="iconfont icon-check-circle" style="font-size:48px"></i>
        <p>暂无待审核用户</p>
      </div>
    </template>

    <div v-else class="user-list">
      <div v-for="item in items" :key="item.user_id" class="user-card">
        <div class="user-card-body">
          <!-- 头部：头像 + 基本信息 -->
          <div class="user-header">
            <div class="user-avatar">{{ item.username.charAt(0).toUpperCase() }}</div>
            <div class="user-detail">
              <span class="user-name">{{ item.username }}</span>
              <span class="user-email">{{ item.email || '未设置邮箱' }}</span>
              <span class="user-meta">
                工号 {{ item.job_number }} · 注册于 {{ formatTime(item.created_at) }}
              </span>
            </div>
          </div>
          <!-- 介绍 -->
          <div v-if="item.bio" class="user-bio">
            <i class="iconfont icon-file"></i>
            {{ item.bio }}
          </div>
        </div>
        <div class="user-card-actions">
          <button class="btn btn-approve" :disabled="actioning === item.user_id" @click="approve(item.user_id)">
            {{ actioning === item.user_id ? '处理中...' : '通过' }}
          </button>
          <button class="btn btn-reject" :disabled="actioning === item.user_id" @click="openReject(item)">
            拒绝
          </button>
        </div>
      </div>
    </div>

    <!-- 拒绝弹窗 -->
    <div v-if="showReject" class="modal-overlay" @click.self="closeReject">
      <div class="modal">
        <h2>拒绝审核</h2>
        <p class="modal-desc">确定要拒绝用户 <strong>{{ rejectTarget?.username }}</strong> 的申请吗？请说明理由，这将通过邮件发送给用户。</p>
        <div class="field">
          <label for="rejectReason">拒绝理由</label>
          <textarea
            id="rejectReason"
            v-model="rejectReason"
            placeholder="请输入拒绝理由..."
            rows="4"
          ></textarea>
        </div>
        <p v-if="rejectError" class="error">{{ rejectError }}</p>
        <div class="modal-actions">
          <button class="btn btn-cancel" @click="closeReject">取消</button>
          <button class="btn btn-reject" :disabled="!rejectReason.trim() || rejecting" @click="confirmReject">
            {{ rejecting ? '提交中...' : '确认拒绝' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { http } from '@/composables/http'

const items = ref([])
const loading = ref(true)
const actioning = ref(null)

// 拒绝弹窗
const showReject = ref(false)
const rejectTarget = ref(null)
const rejectReason = ref('')
const rejectError = ref('')
const rejecting = ref(false)

async function fetchPending() {
  const res = await http('/admin/pending-users?page_size=100')
  if (!res.ok) { items.value = []; return }
  const data = await res.json()
  items.value = data.items
}

onMounted(async () => {
  try {
    await fetchPending()
  } catch {
    items.value = []
  } finally {
    loading.value = false
  }
})

async function approve(userId) {
  actioning.value = userId
  try {
    const res = await http(`/admin/approve-user/${userId}`, { method: 'POST' })
    if (!res.ok) return
    items.value = items.value.filter(i => i.user_id !== userId)
  } catch {
    // http 处理 401
  } finally {
    actioning.value = null
  }
}

function openReject(item) {
  rejectTarget.value = item
  rejectReason.value = ''
  rejectError.value = ''
  showReject.value = true
}

function closeReject() {
  showReject.value = false
  rejectTarget.value = null
  rejectReason.value = ''
  rejectError.value = ''
}

async function confirmReject() {
  if (!rejectReason.value.trim()) return
  rejecting.value = true
  rejectError.value = ''
  try {
    const res = await http(`/admin/reject-user/${rejectTarget.value.user_id}`, {
      method: 'POST',
      body: JSON.stringify({ reason: rejectReason.value }),
    })
    if (!res.ok) { rejectError.value = '操作失败'; return }
    items.value = items.value.filter(i => i.user_id !== rejectTarget.value.user_id)
    closeReject()
  } catch (e) {
    rejectError.value = e.message || '操作失败'
  } finally {
    rejecting.value = false
  }
}

function formatTime(ts) {
  if (!ts) return ''
  const d = new Date(ts * 1000)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}
</script>

<style scoped>
.pending-users { max-width: 720px; }

.page-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 24px;
}

.loading-state {
  color: var(--gray-400);
  font-size: 14px;
  padding: 40px 0;
}

.empty-state {
  text-align: center;
  padding: 64px 0;
  color: var(--gray-300);
}
.empty-state p {
  font-size: 15px;
  margin-top: 16px;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-card {
  background: var(--gray-0);
  border: 1px solid var(--gray-200);
  border-radius: 12px;
  overflow: hidden;
}

.user-card-body {
  padding: 20px 20px 0;
}

.user-header {
  display: flex;
  align-items: center;
  gap: 14px;
}

.user-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: var(--green-deep-100);
  color: var(--green-deep-600);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
}

.user-detail {
  display: flex;
  flex-direction: column;
}
.user-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--gray-900);
}
.user-email {
  font-size: 13px;
  color: var(--gray-400);
}
.user-meta {
  font-size: 12px;
  color: var(--gray-300);
  margin-top: 2px;
}

.user-bio {
  margin: 12px 0 12px 0;
  padding: 12px 14px;
  background: var(--gray-50);
  border-radius: 8px;
  font-size: 13px;
  color: var(--gray-500);
  line-height: 1.6;
  display: flex;
  gap: 8px;
  align-items: flex-start;
}
.user-bio svg {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--gray-300);
}

.user-card-actions {
  padding: 14px 20px;
  border-top: 1px solid var(--gray-100);
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn {
  padding: 8px 20px;
  border-radius: 8px;
  border: 1px solid transparent;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-approve {
  background: var(--green-deep-500);
  color: var(--gray-0);
  border-color: var(--green-deep-500);
}
.btn-approve:hover:not(:disabled) {
  background: var(--green-deep-600);
}

.btn-reject {
  background: var(--gray-0);
  color: var(--red-500);
  border-color: var(--red-200);
}
.btn-reject:hover:not(:disabled) {
  background: var(--red-50);
  border-color: var(--red-300);
}

.btn-cancel {
  background: var(--gray-0);
  color: var(--gray-500);
  border-color: var(--gray-200);
}
.btn-cancel:hover {
  background: var(--gray-50);
}

/* 弹窗 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--gray-0);
  border-radius: 16px;
  padding: 32px;
  width: 460px;
  max-width: 90vw;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
}

.modal h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 8px;
}

.modal-desc {
  font-size: 14px;
  color: var(--gray-500);
  line-height: 1.6;
  margin: 0 0 20px;
}

.field {
  margin-bottom: 12px;
}
.field label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: var(--gray-700);
  font-weight: 500;
}
.field textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  box-sizing: border-box;
  resize: vertical;
}
.field textarea:focus {
  border-color: var(--green-deep-500);
  outline: none;
}

.error {
  color: var(--red-500);
  font-size: 13px;
  margin-bottom: 12px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
