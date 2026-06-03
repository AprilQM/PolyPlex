<template>
    <div class="container">
        <div class="btns">
            <button :class="['nav-btn', { active: isDashboard }]" @click="urlUtils.jump('/workbench/dashboard')">
                <span class="btn-icon iconfont icon-yibiaopan"></span>
                <span class="btn-text">仪表盘</span>
            </button>
            <button :class="['nav-btn', { active: isSquare }]" @click="urlUtils.jump('/workbench/square')">
                <span class="btn-icon iconfont icon-a-mubiaoguangchang"></span>
                <span class="btn-text">项目广场</span>
            </button>
            <button :class="['nav-btn', { active: isProjectManage }]" @click="urlUtils.jump('/workbench/project-manage')">
                <span class="btn-icon iconfont icon-wodexiangmu"></span>
                <span class="btn-text">我的项目</span>
            </button>
            <button :class="['nav-btn', { active: isAssist }]" @click="urlUtils.jump('/workbench/assist')">
                <span class="btn-icon iconfont icon-magic"></span>
                <span class="btn-text">AI协助</span>
            </button>
        </div>
    </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

import '@/assets/icon/workbench_nav/iconfont.css'
import { useUrlUtils } from '@/composables/url'

const route = useRoute()
const router = useRouter()
const urlUtils = useUrlUtils(router)

const isDashboard = computed(() => route.path === '/workbench/dashboard')
const isSquare = computed(() => route.path === '/workbench/square')
const isProjectManage = computed(() => route.path === '/workbench/project-manage')
const isAssist = computed(() => route.path === '/workbench/assist')
</script>

<style scoped>
.container {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background-color: var(--gray-0);
    border-top: 1px solid var(--gray-200);
    display: none;
    z-index: 100;
    padding: 0 8px;
}

@media screen and (max-width: 768px) {
    .container {
        display: block;
    }
}

.btns {
    height: 100%;
    display: flex;
    align-items: stretch;
    gap: 4px;
}

.nav-btn {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    border: none;
    background: transparent;
    color: var(--gray-400);
    cursor: pointer;
    transition: all 0.2s ease;
    padding: 4px 0;
    position: relative;
}

.nav-btn:hover {
    color: var(--gray-600);
}

.nav-btn.active {
    color: var(--green-deep-600);
}

.btn-icon {
    font-size: 22px;
    transition: transform 0.2s ease;
}

.nav-btn.active .btn-icon {
    transform: scale(1.1);
}

.btn-text {
    font-size: 11px;
    font-weight: 500;
    white-space: nowrap;
}
</style>
