<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <router-link to="/home" class="logo">PolyPlex</router-link>
        <span class="badge">管理后台</span>
      </div>

      <nav class="nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
        >
          <i class="iconfont" :class="'icon-' + item.icon"></i>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="admin-info">
          <span class="admin-name">{{ userStore.username }}</span>
        </div>
        <button class="back-btn" @click="handleBack">
          <i class="iconfont icon-arrow-left"></i>
          返回工作台
        </button>
        <button class="logout-btn" @click="handleLogout">
          <i class="iconfont icon-logout"></i>
          退出登录
        </button>
      </div>
    </aside>

    <!-- 主内容 -->
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import '@/assets/icon/admin/iconfont.css'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const navItems = [
  {
    path: '/admin/dashboard',
    label: '仪表盘',
    icon: 'dashboard',
  },
  {
    path: '/admin/pending-users',
    label: '用户审核',
    icon: 'user-check',
  },
  {
    path: '/admin/users',
    label: '用户管理',
    icon: 'users',
  },
]

function isActive(path) {
  return route.path === path
}

function handleBack() {
  router.push('/workbench/dashboard')
}

function handleLogout() {
  userStore.logout()
  router.push('/home')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  background: var(--gray-50);
}

/* 侧边栏 */
.sidebar {
  width: 240px;
  background: var(--gray-900);
  color: var(--gray-0);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 24px 20px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  color: var(--gray-0);
  text-decoration: none;
}

.badge {
  font-size: 10px;
  background: var(--green-deep-500);
  color: var(--gray-0);
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* 导航 */
.nav {
  flex: 1;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  color: var(--gray-300);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.15s;
}
.nav-item:hover {
  background: rgba(255,255,255,0.06);
  color: var(--gray-0);
}
.nav-item.active {
  background: var(--green-deep-500);
  color: var(--gray-0);
}

.nav-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

/* 底部 */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255,255,255,0.08);
}

.admin-info {
  margin-bottom: 8px;
}

.admin-name {
  font-size: 13px;
  color: var(--gray-400);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  background: rgba(255,255,255,0.04);
  color: var(--gray-400);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}
.back-btn:hover {
  background: rgba(255,255,255,0.08);
  color: var(--gray-0);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  background: rgba(255,255,255,0.04);
  color: var(--gray-500);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
  margin-top: 4px;
}
.logout-btn:hover {
  background: rgba(239,68,68,0.12);
  color: var(--red-400);
}

/* 主内容 */
.main {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}
</style>
