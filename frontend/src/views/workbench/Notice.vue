<template>
    <div class="container">
        
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

import { useSecondaryNavStore } from '@/stores/useSecondaryNavStore'

const secondaryNavStore = useSecondaryNavStore()

onMounted(() => {
    secondaryNavStore.width = 280
    secondaryNavStore.content = []
    secondaryNavStore.switchNew()
})
</script>

<style scoped>
.container {
    
}
</style>