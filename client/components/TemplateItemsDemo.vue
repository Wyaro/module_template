<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import SelectBox from '@/components/SelectBox.vue'
import SearchInput from '@/components/SearchInput.vue'
import LoadingContentArea from '@/components/LoadingContentArea.vue'
import { apiClient } from '@/js/api/manager'
import { useToast } from '@/js/utils/toast.js'
import { logError } from '@/js/utils/logError.js'

import { moduleTemplateEndpoints } from '../js/endpoints'

const { t } = useI18n()
const toast = useToast()

const items = ref([])
const loading = ref(false)
const searchQuery = ref('')
const activeFilter = ref('all')

const activeOptions = computed(() => [
  { id: 'all', name: t('module_template.items.filterAll') },
  { id: 'true', name: t('module_template.items.filterActive') },
  { id: 'false', name: t('module_template.items.filterInactive') },
])

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
      toast.warning(response.message || t('module_template.items.loadFail'))
    }
  } catch (error) {
    logError('TemplateItemsDemo.fetchItems', error)
    toast.error(t('module_template.items.loadError'))
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
      <h2 class="h5 mb-2">{{ t('module_template.items.title') }}</h2>
      <p class="text-muted small mb-3">
        {{ t('module_template.items.description') }}
      </p>
      <div class="d-flex flex-wrap gap-2 mb-3 align-items-end">
        <div style="min-width: 180px;">
          <label class="form-label small mb-1">{{ t('module_template.items.status') }}</label>
          <SelectBox
            v-model="activeFilter"
            :options="activeOptions"
            value-key="id"
            label-key="name"
            :include-all-option="false"
          />
        </div>
        <SearchInput
          v-model="searchQuery"
          :placeholder="t('module_template.items.searchPlaceholder')"
          layout="grow"
          :show-icon="true"
          @update:model-value="fetchItems"
        />
      </div>
      <LoadingContentArea :loading="loading" min-height="6rem" :loading-text="t('module_template.loading')">
        <ul v-if="filteredItems.length" class="list-group list-group-flush">
          <li
            v-for="item in filteredItems"
            :key="item.public_id"
            class="list-group-item px-0 d-flex justify-content-between align-items-center"
          >
            <span>{{ item.name }}</span>
            <span class="badge" :class="item.active ? 'text-bg-success' : 'text-bg-secondary'">
              {{ item.active ? t('module_template.items.active') : t('module_template.items.inactive') }}
            </span>
          </li>
        </ul>
        <p v-else class="text-muted small mb-0">{{ t('module_template.items.empty') }}</p>
      </LoadingContentArea>
    </div>
  </section>
</template>
