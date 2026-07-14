<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import SelectBox from '@/components/SelectBox.vue'
import SearchInput from '@/components/SearchInput.vue'
import { apiClient } from '@/js/api/manager'
import { useToast } from '@/js/utils/toast.js'

import { moduleTemplateEndpoints } from '../js/endpoints'

const toast = useToast()

const items = ref([])
const loading = ref(false)
const searchQuery = ref('')
const activeFilter = ref('all')

const ACTIVE_OPTIONS = [
  { id: 'all', name: 'Все' },
  { id: 'true', name: 'Активные' },
  { id: 'false', name: 'Неактивные' },
]

const filteredItems = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) {
    return items.value
  }
  return items.value.filter((item) => (item.name || '').toLowerCase().includes(q))
})

const fetchItems = async () => {
  loading.value = true
  try {
    const params = {}
    if (activeFilter.value !== 'all') {
      params.active = activeFilter.value
    }
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }
    const response = await apiClient.get(moduleTemplateEndpoints.moduleTemplate.items, { params })
    if (response.success) {
      const data = response.data
      items.value = Array.isArray(data) ? data : (data?.results || [])
    } else {
      toast.warning(response.message || 'Не удалось загрузить элементы')
    }
  } catch (error) {
    logError(error, { source: 'TemplateItemsDemo.fetchItems' })
    toast.error('Ошибка при загрузке элементов')
  } finally {
    loading.value = false
  }
}

watch(activeFilter, () => {
  fetchItems()
})

onMounted(() => {
  fetchItems()
})
</script>

<template>
  <section class="mt-items-demo card border-0 shadow-sm">
    <div class="card-body">
      <h2 class="h5 mb-2">Учебный список TemplateItem</h2>
      <p class="text-muted small mb-3">
        Пример SelectBox и SearchInput из ядра + CRUD API по public_id.
      </p>
      <div class="d-flex flex-wrap gap-2 mb-3 align-items-end">
        <div style="min-width: 180px;">
          <label class="form-label small mb-1">Статус</label>
          <SelectBox
            v-model="activeFilter"
            :options="ACTIVE_OPTIONS"
            value-key="id"
            label-key="name"
            :include-all-option="false"
          />
        </div>
        <SearchInput
          v-model="searchQuery"
          placeholder="Поиск по названию..."
          layout="grow"
          :show-icon="true"
          @update:model-value="fetchItems"
        />
      </div>
      <div v-if="loading" class="text-muted small">Загрузка...</div>
      <ul v-else-if="filteredItems.length" class="list-group list-group-flush">
        <li
          v-for="item in filteredItems"
          :key="item.public_id"
          class="list-group-item px-0 d-flex justify-content-between align-items-center"
        >
          <span>{{ item.name }}</span>
          <span class="badge" :class="item.active ? 'text-bg-success' : 'text-bg-secondary'">
            {{ item.active ? 'активен' : 'неактивен' }}
          </span>
        </li>
      </ul>
      <p v-else class="text-muted small mb-0">Элементы не найдены.</p>
    </div>
  </section>
</template>
