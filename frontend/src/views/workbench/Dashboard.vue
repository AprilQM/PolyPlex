<template>
    <div class="container">
        
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

import { useSecondaryNavStore } from '@/stores/useSecondaryNavStore'

const secondaryNavStore = useSecondaryNavStore()

onMounted(() => {
    secondaryNavStore.width = 400
    secondaryNavStore.content = [
        {
            title: '第一部分',
            borderBottom: true,
            content: [
                {
                    text: '第一部分第一项',
                    icon: '🏠',
                    active: true,
                    command: () => {
                        secondaryNavStore.switchGlobal(0, 0)
                    }
                },
                {
                    text: '第一部分第二项',
                    icon: '📊',
                    active: false,
                    command: () => {
                        secondaryNavStore.switchGlobal(0, 1)
                    }
                }
            ]
        },
        {
            title: '第二部分',
            borderBottom: false,
            content: [
                {
                    text: '第二部分第一项',
                    icon: '🕒',
                    active: false,
                    command: () => {
                        secondaryNavStore.switchGlobal(1, 0)
                    }
                },
                {
                    text: '第二部分第二项',
                    icon: '📅',
                    active: false,
                    command: () => {
                        secondaryNavStore.switchInPart(1, 1)
                    }
                }
            ]
        }
    ]
    secondaryNavStore.switchNew()
})
</script>

<style scoped>
</style>