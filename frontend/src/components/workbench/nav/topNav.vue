<template>
    <div class="container">
        <div class="left">
            <div class="logo">
                <img src="@/assets/image/logo/PolyPlex-logo.svg">
                <span class="logo-text">PolyPlex</span>
                <span class="version">v0.1.0</span>
            </div>
        </div>
        <nav class="nav">
            <button :class="['nav-btn', { active: isDashboard }]" @click="urlUtils.jump('/workbench/dashboard')">
                <i class="btn-icon iconfont icon-yibiaopan"></i>
                <span class="btn-text">仪表盘</span>
            </button>
            <button :class="['nav-btn', { active: isSquare }]" @click="urlUtils.jump('/workbench/square')">
                <i class="btn-icon iconfont icon-a-mubiaoguangchang"></i>
                <span class="btn-text">项目广场</span>
            </button>
            <button :class="['nav-btn', { active: isProjectManage }]" @click="urlUtils.jump('/workbench/project-manage')">
                <i class="btn-icon iconfont icon-wodexiangmu"></i>
                <span class="btn-text">我的项目</span>
            </button>
            <button :class="['nav-btn', { active: isAssist }]" @click="urlUtils.jump('/workbench/assist')">
                <i class="btn-icon iconfont icon-magic"></i>
                <span class="btn-text">AI协助</span>
            </button>
        </nav>
        <div class="right">
            <button :class="['notif-btn', 'iconfont', 'icon-tongzhi', { 'has-notice': userStore.hasUnreadMessage }]"
                @click="urlUtils.jump('/workbench/notice')"></button>
            <div class="user">
                <img :src="userStore.avatar" @error="handleAvatarError" class="avatar"
                    @click="urlUtils.jump('/workbench/user-space/' + userStore.id)">
                <div class="user-info">
                    <span class="username" @click="urlUtils.jump('/workbench/user-space/' + userStore.id)">{{ userStore.username }}</span>
                    <span class="email">{{ userStore.email }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

import '@/assets/icon/workbench_nav/iconfont.css'
import { useUrlUtils } from '@/composables/url'
import { useUserStore } from '@/stores/useUserStore'
import defaultAvatar from '@/assets/image/user/default_avatar.png'

const route = useRoute()
const router = useRouter()
const urlUtils = useUrlUtils(router)
const userStore = useUserStore()

const isDashboard = computed(() => route.path === '/workbench/dashboard')
const isSquare = computed(() => route.path === '/workbench/square')
const isProjectManage = computed(() => route.path === '/workbench/project-manage')
const isAssist = computed(() => route.path === '/workbench/assist')

const handleAvatarError = (e) => {
    e.target.src = defaultAvatar
}
</script>

<style scoped>
/* ============= Container ============= */
.container {
    width: 100%;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    top: 0;
    left: 0;
    padding: 0 24px;
    background-color: var(--gray-0);
    border-bottom: 1px solid var(--gray-200);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    z-index: 100;
}

/* ============= Left: Logo ============= */
.left {
    display: flex;
    align-items: center;
    flex-shrink: 0;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo img {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(26, 77, 62, 0.18);
}

.logo-text {
    font-size: 22px;
    font-weight: 700;
    background: linear-gradient(135deg, var(--green-deep-500) 0%, var(--peach-500) 100%);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    letter-spacing: -0.3px;
}

.version {
    font-size: 11px;
    font-weight: 600;
    color: var(--gray-400);
    background: var(--gray-100);
    padding: 2px 10px;
    border-radius: 20px;
    white-space: nowrap;
}

/* ============= Center: Nav ============= */
.nav {
    display: flex;
    align-items: center;
    gap: 4px;
    flex: 1;
    justify-content: center;
    padding: 0 16px;
}

.nav-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--gray-500);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.nav-btn:hover {
    background: var(--gray-50);
    color: var(--gray-700);
}

.nav-btn.active {
    background: var(--green-deep-50);
    color: var(--green-deep-700);
    font-weight: 600;
}

.btn-icon {
    font-size: 18px;
    line-height: 1;
}

/* ============= Right: User Area ============= */
.right {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0;
}

.notif-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background: transparent;
    color: var(--gray-500);
    font-size: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.notif-btn:hover {
    background: var(--gray-50);
    color: var(--gray-700);
}

.notif-btn::after {
    content: '';
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--peach-500);
    position: absolute;
    top: 6px;
    right: 6px;
    display: none;
    box-shadow: 0 0 0 2px var(--gray-0);
}

.has-notice::after {
    display: block;
}

.user {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    padding: 4px 8px 4px 4px;
    border-radius: 24px;
    transition: background 0.2s ease;
}

.user:hover {
    background: var(--gray-50);
}

.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.user-info {
    display: flex;
    flex-direction: column;
    line-height: 1.3;
}

.username {
    font-size: 14px;
    font-weight: 600;
    color: var(--gray-800);
}

.email {
    font-size: 11px;
    color: var(--gray-400);
}

/* ============= Responsive ============= */
@media screen and (max-width: 1040px) {
    .container {
        padding: 0 16px;
    }
    .nav-btn {
        padding: 8px 12px;
    }
    .btn-text {
        display: none;
    }
    .user-info {
        display: none;
    }
    .logo-text {
        font-size: 18px;
    }
}

@media screen and (max-width: 768px) {
    .nav {
        display: none;
    }
}

@media screen and (max-width: 570px) {
    .version {
        display: none;
    }
}

@media screen and (max-width: 430px) {
    .logo-text {
        display: none;
    }
    .logo img {
        width: 34px;
        height: 34px;
    }
}
</style>
