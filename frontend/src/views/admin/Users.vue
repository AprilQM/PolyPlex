<template>
  <div class="users-page">
    <h1 class="page-title">用户管理</h1>

    <!-- 搜索 -->
    <div class="toolbar">
      <div class="search-box">
        <i class="iconfont icon-search"></i>
        <input
          v-model="search"
          type="text"
          placeholder="搜索用户名或邮箱..."
          @keyup.enter="doSearch"
        />
      </div>
      <button class="btn-search" @click="doSearch">搜索</button>
    </div>

    <div v-if="loading" class="loading-state">加载中...</div>

    <template v-else-if="items.length === 0">
      <div class="empty-state">
        <p>{{ search ? '未找到匹配的用户' : '暂无用户' }}</p>
      </div>
    </template>

    <div v-else class="user-table-wrap">
      <table class="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>工号</th>
            <th>状态</th>
            <th>注册时间</th>
            <th>最后登录</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in items" :key="u.id">
            <td class="cell-id">{{ u.id }}</td>
            <td>
              <div class="cell-user">
                <span class="user-avatar-sm">{{ u.username.charAt(0).toUpperCase() }}</span>
                {{ u.username }}
              </div>
            </td>
            <td class="cell-email">{{ u.email }}</td>
            <td class="cell-job">{{ u.job_number }}</td>
            <td>
              <span v-if="u.is_system" class="tag tag-system">系统</span>
              <span v-if="u.is_admin" class="tag tag-admin">管理员</span>
              <span v-if="u.is_pending" class="tag tag-pending">待审核</span>
              <span v-if="u.is_rejected" class="tag tag-rejected">未通过</span>
              <span v-if="u.is_banned" class="tag tag-ban">封禁</span>
              <span v-if="!u.is_admin && !u.is_pending && !u.is_rejected && !u.is_banned && !u.is_system" class="tag tag-normal">正常</span>
            </td>
            <td class="cell-date">{{ formatTime(u.created_at) }}</td>
            <td class="cell-date">{{ formatTime(u.login_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div v-if="total > pageSize" class="pagination">
      <button :disabled="page <= 1" @click="goPage(page - 1)">上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button :disabled="page >= totalPages" @click="goPage(page + 1)">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { http } from '@/composables/http'

const items = ref([])
const loading = ref(true)
const page = ref(1)
const pageSize = 20
const total = ref(0)
const search = ref('')

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

async function fetchUsers() {
  loading.value = true
  try {
    const params = new URLSearchParams({ page: page.value, page_size: pageSize })
    if (search.value) params.set('search', search.value)
    const res = await http(`/admin/users?${params}`)
    if (!res.ok) { items.value = []; total.value = 0; return }
    const data = await res.json()
    items.value = data.items
    total.value = data.total
  } catch {
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function doSearch() {
  page.value = 1
  fetchUsers()
}

function goPage(p) {
  page.value = p
  fetchUsers()
}

onMounted(fetchUsers)

function formatTime(ts) {
  if (!ts) return '-'
  const d = new Date(ts * 1000)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}
</script>

<style scoped>
.users-page { max-width: 960px; }

.page-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 24px;
}

/* 工具栏 */
.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--gray-0);
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 8px 14px;
  color: var(--gray-400);
}
.search-box input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: var(--gray-900);
  background: transparent;
}
.search-box input::placeholder {
  color: var(--gray-300);
}

.btn-search {
  padding: 8px 20px;
  background: var(--green-deep-500);
  color: var(--gray-0);
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
}
.btn-search:hover {
  background: var(--green-deep-600);
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
  font-size: 15px;
}

/* 表格 */
.user-table-wrap {
  background: var(--gray-0);
  border: 1px solid var(--gray-200);
  border-radius: 12px;
  overflow: hidden;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
.user-table th {
  text-align: left;
  padding: 12px 16px;
  background: var(--gray-50);
  color: var(--gray-500);
  font-weight: 500;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--gray-200);
}
.user-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--gray-100);
  color: var(--gray-700);
}
.user-table tr:last-child td {
  border-bottom: none;
}

.cell-id { color: var(--gray-400); font-size: 12px; font-family: monospace; }
.cell-email { color: var(--gray-400); }
.cell-job { color: var(--gray-500); font-family: monospace; }
.cell-date { color: var(--gray-400); font-size: 13px; }

.cell-user {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar-sm {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--green-deep-100);
  color: var(--green-deep-600);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

/* 标签 */
.tag {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}
.tag-system { background: var(--purple-50); color: var(--purple-500); }
.tag-admin { background: var(--green-deep-50); color: var(--green-deep-600); }
.tag-pending { background: var(--yellow-50); color: var(--yellow-500); }
.tag-rejected { background: var(--orange-50); color: var(--orange-600); }
.tag-ban { background: var(--red-50); color: var(--red-500); }
.tag-normal { background: var(--gray-100); color: var(--gray-500); }

/* 分页 */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
}
.pagination button {
  padding: 6px 16px;
  border: 1px solid var(--gray-200);
  border-radius: 6px;
  background: var(--gray-0);
  color: var(--gray-600);
  font-size: 13px;
  cursor: pointer;
}
.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.pagination button:hover:not(:disabled) {
  border-color: var(--green-deep-500);
  color: var(--green-deep-500);
}
.page-info {
  font-size: 13px;
  color: var(--gray-400);
}
</style>
