<template>
    <div class="container">
        <topNav></topNav>
        <leftNav></leftNav>
        <router-view></router-view>
        <bottomNav></bottomNav>
    </div>
</template>

<script setup>
import router from '@/router';
import { ref, reactive, computed, onMounted } from 'vue'

import topNav from '@/components/workbench/nav/topNav.vue'
import leftNav from '@/components/workbench/nav/leftNav.vue'
import bottomNav from '@/components/workbench/nav/bottomNav.vue'

</script>

<style scoped>
.container {
    
}
</style>