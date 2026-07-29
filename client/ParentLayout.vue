<template>
    <div class="module-template-layout">
        <router-view :key="$route.name" />
    </div>
</template>

<script setup>
</script>

<style scoped>
.module-template-layout {
    min-height: 100%;
    width: 100%;
}
</style>
