<template>
  <div class="dashboard">
    <h1 class="page-title">仪表盘</h1>

    <div v-if="loading" class="loading-state">加载中...</div>

    <div v-else class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon users">
          <i class="iconfont icon-users" style="font-size:24px"></i>
        </div>
        <div class="stat-body">
          <span class="stat-value">{{ stats.total_users }}</span>
          <span class="stat-label">注册用户</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon pending">
          <i class="iconfont icon-check-circle" style="font-size:24px"></i>
        </div>
        <div class="stat-body">
          <span class="stat-value">{{ stats.pending_users }}</span>
          <span class="stat-label">待审核</span>
        </div>
      </div>
    </div>

    <div v-if="!loading && stats.pending_users > 0" class="quick-actions">
      <h2>快速操作</h2>
      <router-link to="/admin/pending-users" class="quick-link">
        前往审核 {{ stats.pending_users }} 位待审核用户 →
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { http } from '@/composables/http'

const loading = ref(true)
const stats = ref({ total_users: 0, pending_users: 0 })

onMounted(async () => {
  try {
    const res = await http('/admin/stats')
    if (res.ok) stats.value = await res.json()
  } catch {
    // http 会处理 401 自动登出
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard { max-width: 800px; }

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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--gray-0);
  border: 1px solid var(--gray-200);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stat-icon.users { background: var(--blue-50); color: var(--blue-500); }
.stat-icon.pending { background: var(--yellow-50); color: var(--yellow-500); }

.stat-body {
  display: flex;
  flex-direction: column;
}
.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--gray-900);
  line-height: 1.2;
}
.stat-label {
  font-size: 13px;
  color: var(--gray-400);
}

.quick-actions {
  background: var(--gray-0);
  border: 1px solid var(--gray-200);
  border-radius: 12px;
  padding: 24px;
}
.quick-actions h2 {
  font-size: 16px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 12px;
}
.quick-link {
  color: var(--green-deep-500);
  font-size: 14px;
  text-decoration: none;
}
.quick-link:hover {
  text-decoration: underline;
}
</style>
