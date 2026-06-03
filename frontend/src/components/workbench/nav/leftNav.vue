<template>
    <div class="container" :style="{
        width: secondaryNavStore._width + 'px',
        left: show ? '0' : '-' + secondaryNavStore._width + 'px',
        '--x': secondaryNavStore._x
    }">
        <div :class="['toggle-in-mobile', 'iconfont', 'icon-youjiantou', show ? 'toggle-hidden' : 'toggle-show']"
            @click="show = !show"></div>
        <div class="display">
            <div class="part" v-for="part in secondaryNavStore._content" :key="part.partTitle">
                <span class="part-title">{{ part.title }}</span>
                <div :class="['btns', { 'has-border-bottom': part.borderBottom }]">
                    <button v-for="btn in part.content" :key="btn.text" @click="btn.command"
                        :class="{ active: btn.active }">
                        <span>{{ btn.icon }}</span>
                        {{ btn.text }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useSecondaryNavStore } from '@/stores/useSecondaryNavStore'

const secondaryNavStore = useSecondaryNavStore()

const show = ref(true)

const handleResize = () => {
    show.value = window.innerWidth > 1040
}

onMounted(() => {
    handleResize()
    window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.container {
    position: fixed;
    top: 60px;
    left: 0;
    height: calc(100% - 60px);
    background-color: var(--gray-0);
    border-right: 1px solid var(--gray-200);
    transition: 0.3s transform ease, 0.3s left ease;
    transform: translateX(var(--x));
    padding: 12px 8px;
    z-index: 99;
    overflow: visible;
}

.display {
    width: 100%;
    height: 100%;
    overflow-y: auto;
}

.part-title {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--gray-400);
    padding: 8px 12px 4px;
    display: block;
}

.btns {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: 0 8px;
    position: relative;
}

.has-border-bottom {
    padding-bottom: 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--gray-200);
}

.btns button {
    padding: 8px 12px;
    background: transparent;
    border-radius: 8px;
    border: none;
    color: var(--gray-600);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
    display: flex;
    align-items: center;
    gap: 8px;
}

.btns button:hover {
    background: var(--gray-50);
    color: var(--gray-800);
}

.btns button.active {
    background: var(--green-deep-50);
    color: var(--green-deep-700);
    font-weight: 600;
}

.btns button span {
    font-size: 18px;
}

/* ============= Toggle (mobile) ============= */
.toggle-in-mobile {
    position: absolute;
    top: 32px;
    right: -44px;
    background: var(--gray-0);
    width: 44px;
    height: 44px;
    display: none;
    align-items: center;
    justify-content: center;
    border-radius: 0 12px 12px 0;
    border: 1px solid var(--gray-200);
    border-left: none;
    cursor: pointer;
    z-index: -1;
    color: var(--gray-500);
    font-size: 16px;
    transition: color 0.2s ease;
}

.toggle-in-mobile:hover {
    color: var(--green-deep-500);
}

.toggle-in-mobile::before {
    transition: transform 0.3s ease;
}

.toggle-show::before {
    transform: rotate(0deg);
}

.toggle-hidden::before {
    transform: rotate(180deg);
}

@media screen and (max-width: 1040px) {
    .toggle-in-mobile {
        display: flex;
    }
}
</style>
