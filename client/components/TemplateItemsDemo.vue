<script setup>
/**
 * Учебный блок CRUD TemplateItem на StatusPage.
 * Компоненты ядра: SearchInput, SelectBox, DataTable, LoadingContentArea, ModalCenter, confirm.
 */
import { computed, defineAsyncComponent, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Pencil, Plus, Trash2 } from 'lucide-vue-next'
import DataTable from '@/components/DataTable.vue'
import LoadingContentArea from '@/components/LoadingContentArea.vue'
import SearchInput from '@/components/SearchInput.vue'
import SelectBox from '@/components/SelectBox.vue'
import { apiClient } from '@/js/api/manager'
import { confirmDelete } from '@/js/utils/confirm.js'
import { logError } from '@/js/utils/logError.js'
import { useToast } from '@/js/utils/toast.js'

import { moduleTemplateEndpoints } from '../js/endpoints'

const TemplateItemModal = defineAsyncComponent(() =>
  import('./TemplateItemModal.vue'),
)

const { t } = useI18n()
const toast = useToast()

const isLoading = ref(false)
const rows = ref([])
const totalItems = ref(0)
const rowsPerPage = ref(12)
const currentPage = ref(1)
const searchQuery = ref('')
const activeFilter = ref('all')
const showModal = ref(false)
const editingItem = ref(null)
let searchTimer = null

const activeOptions = computed(() => [
  { id: 'all', name: t('module_template.items.filterAll') },
  { id: 'true', name: t('module_template.items.filterActive') },
  { id: 'false', name: t('module_template.items.filterInactive') },
])

const columns = computed(() => [
  { key: 'name', label: t('module_template.items.name') },
  { key: 'description', label: t('module_template.items.descriptionCol'), hideBelow: 'md' },
  {
    key: 'active',
    label: t('module_template.items.status'),
    headerStyle: { textAlign: 'center' },
    cellStyle: { textAlign: 'center' },
  },
  {
    key: 'actions',
    label: t('module_template.items.actions'),
    headerStyle: { textAlign: 'right' },
    cellStyle: { textAlign: 'right' },
  },
])

const getItemKey = (item) => item.public_id

const tableEmptyText = computed(() => {
  if (searchQuery.value.trim() || activeFilter.value !== 'all') {
    return t('module_template.items.notFound')
  }
  return t('module_template.items.empty')
})

const itemsUrl = moduleTemplateEndpoints.moduleTemplate.items

const loadItems = async () => {
  isLoading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: rowsPerPage.value,
    }
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }
    if (activeFilter.value !== 'all') {
      params.active = activeFilter.value
    }
    const response = await apiClient.get(itemsUrl, { params })
    if (!response.success) {
      toast.warning(response.message || t('module_template.items.loadFail'))
      rows.value = []
      totalItems.value = 0
      return
    }
    const data = response.data
    if (Array.isArray(data)) {
      rows.value = data
      totalItems.value = data.length
    } else {
      rows.value = data?.results || []
      totalItems.value = data?.count ?? rows.value.length
    }
  } catch (error) {
    logError('TemplateItemsDemo.loadItems', error)
    toast.error(t('module_template.items.loadError'))
    rows.value = []
    totalItems.value = 0
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadItems()
})

watch(activeFilter, () => {
  currentPage.value = 1
  loadItems()
})

const handlePageChange = (page) => {
  currentPage.value = Number(page)
  loadItems()
}

const handleSearchQuery = (query) => {
  searchQuery.value = query
  if (searchTimer) {
    clearTimeout(searchTimer)
  }
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    loadItems()
  }, 300)
}

const openCreateModal = () => {
  editingItem.value = null
  showModal.value = true
}

const openEditModal = (item) => {
  editingItem.value = item
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingItem.value = null
}

const onItemSaved = async () => {
  closeModal()
  await loadItems()
}

const deleteItem = async (item) => {
  const ok = await confirmDelete(
    t('module_template.items.deleteTitle'),
    t('module_template.items.deleteMessage', { name: item.name }),
  )
  if (!ok) {
    return
  }
  try {
    const response = await apiClient.delete(`${itemsUrl}${item.public_id}/`)
    if (response.success) {
      toast.success(t('module_template.items.deleteSuccess'))
      await loadItems()
    } else {
      toast.warning(response.message || t('module_template.items.deleteFail'))
    }
  } catch (error) {
    logError('TemplateItemsDemo.deleteItem', error)
    toast.error(t('module_template.items.deleteError'))
  }
}
</script>

<template>
  <section class="mt-items-demo">
    <header class="mt-items-demo__header">
      <div>
        <h2 class="mt-items-demo__title">{{ t('module_template.items.title') }}</h2>
        <p class="mt-items-demo__subtitle">{{ t('module_template.items.description') }}</p>
      </div>
      <button
        type="button"
        class="btn btn-primary btn-sm d-inline-flex align-items-center gap-2"
        @click="openCreateModal"
      >
        <Plus :size="14" />
        {{ t('module_template.items.create') }}
      </button>
    </header>

    <div class="mt-items-demo__toolbar">
      <SearchInput
        :model-value="searchQuery"
        :placeholder="t('module_template.items.searchPlaceholder')"
        layout="grow"
        :show-icon="true"
        @update:model-value="handleSearchQuery"
      />
      <div class="mt-items-demo__filter">
        <SelectBox
          v-model="activeFilter"
          :options="activeOptions"
          value-key="id"
          label-key="name"
          :include-all-option="false"
        />
      </div>
    </div>

    <LoadingContentArea
      :loading="isLoading"
      min-height="8rem"
      :loading-text="t('module_template.loading')"
    >
      <DataTable
        :columns="columns"
        :items="rows"
        :get-item-key="getItemKey"
        :empty-text="tableEmptyText"
        :enable-pagination="true"
        :current-page="currentPage"
        :items-per-page="rowsPerPage"
        :total-items="totalItems"
        @update:current-page="handlePageChange"
      >
        <template #cell-description="{ item }">
          <span class="text-muted">{{ item.description || '—' }}</span>
        </template>
        <template #cell-active="{ item }">
          <span
            class="badge"
            :class="item.active ? 'text-bg-success' : 'text-bg-secondary'"
          >
            {{ item.active ? t('module_template.items.active') : t('module_template.items.inactive') }}
          </span>
        </template>
        <template #cell-actions="{ item }">
          <div class="mt-items-demo__actions">
            <button
              type="button"
              class="btn btn-sm btn-outline-secondary"
              :title="t('module_template.items.edit')"
              @click="openEditModal(item)"
            >
              <Pencil :size="14" />
            </button>
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              :title="t('module_template.items.delete')"
              @click="deleteItem(item)"
            >
              <Trash2 :size="14" />
            </button>
          </div>
        </template>
      </DataTable>
    </LoadingContentArea>

    <TemplateItemModal
      v-if="showModal"
      :visible="showModal"
      :item="editingItem"
      @close="closeModal"
      @saved="onItemSaved"
    />
  </section>
</template>

<style scoped lang="scss">
.mt-items-demo {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 0.5rem;
  background: var(--ui-surface, var(--bs-body-bg));
  border: 1px solid var(--ui-border, var(--bs-border-color));
}

.mt-items-demo__header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
}

.mt-items-demo__title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--ui-text, var(--bs-body-color));
}

.mt-items-demo__subtitle {
  margin: 0.25rem 0 0;
  color: var(--ui-text-muted, var(--bs-secondary-color));
  font-size: 0.85rem;
  max-width: 36rem;
}

.mt-items-demo__toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 0.75rem;
}

.mt-items-demo__filter {
  flex: 0 0 160px;
  min-width: 140px;
}

.mt-items-demo__actions {
  display: inline-flex;
  gap: 0.35rem;
  justify-content: flex-end;
}

.mt-items-demo__toolbar :deep(.select-box) {
  --select-box-font-size: 0.875rem;
}
</style>
