<script setup>
/**
 * Учебный блок CRUD TemplateItem на StatusPage.
 * Компоненты ядра: SearchInput, SelectBox, DataTable, DropDown, FormCard/FormField,
 * LoadingContentArea, ModalCenter, confirm. Состояние списка — useRouteQueryState.
 */
import { computed, defineAsyncComponent, onMounted, ref } from 'vue'
import { Download, MoreHorizontal, Pencil, Plus, Trash2 } from '@lucide/vue'
import DataTable from '@/components/DataTable.vue'
import DropDown from '@/components/DropDown.vue'
import LoadingContentArea from '@/components/LoadingContentArea.vue'
import SearchInput from '@/components/SearchInput.vue'
import SelectBox from '@/components/SelectBox.vue'
import { useRouteQueryState } from '@/composables/useRouteQueryState.js'
import { useAppI18n } from '@/i18n/useAppI18n.js'
import { apiClient } from '@/js/api/manager'
import { confirmDelete } from '@/js/utils/confirm.js'
import { downloadMedia } from '@/js/utils/mediaDownload.js'
import { logError } from '@/js/utils/logError.js'
import { useToast } from '@/js/utils/toast.js'

import { moduleTemplateEndpoints } from '../js/endpoints'

const TemplateItemModal = defineAsyncComponent(() =>
  import('./TemplateItemModal.vue'),
)

const { t } = useAppI18n()
const toast = useToast()

const isLoading = ref(false)
const rows = ref([])
const totalItems = ref(0)
const rowsPerPage = ref(12)
const showModal = ref(false)
const editingItem = ref(null)
const isQueryWatchReady = ref(false)

const { state: listState, patchState, watchState } = useRouteQueryState({
  q: { default: '' },
  page: { default: 1, type: 'number' },
  active: { default: 'all', enum: ['all', 'true', 'false'] },
}, { debounceKeys: ['q'] })

const searchQuery = computed(() => listState.value.q)
const currentPage = computed(() => listState.value.page)
const activeFilter = computed({
  get: () => listState.value.active,
  set: (value) => {
    patchState({ active: value }, { immediate: true })
  },
})

const activeOptions = computed(() => [
  { id: 'all', name: t('module_template.items.filterAll') },
  { id: 'true', name: t('module_template.items.filterActive') },
  { id: 'false', name: t('module_template.items.filterInactive') },
])

const columns = computed(() => [
  { key: 'name', label: t('module_template.items.name') },
  { key: 'description', label: t('module_template.items.descriptionCol'), hideBelow: 'md' },
  {
    key: 'attachment',
    label: t('module_template.items.attachment'),
    hideBelow: 'md',
  },
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
      params.q = searchQuery.value.trim()
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

onMounted(async () => {
  await loadItems()
  isQueryWatchReady.value = true
})

watchState(() => {
  if (!isQueryWatchReady.value) {
    return
  }
  loadItems()
})

const handlePageChange = (page) => {
  patchState({ page: Number(page) }, { immediate: true })
}

const handleSearchQuery = (query) => {
  patchState({ q: query })
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

const downloadAttachment = async (item) => {
  if (!item?.attachment_url) {
    return
  }
  try {
    await downloadMedia(item.attachment_url, { filename: item.attachment_name || undefined })
  } catch (error) {
    logError('TemplateItemsDemo.downloadAttachment', error)
    toast.error(t('module_template.items.attachmentDownloadError'))
  }
}
</script>

<template>
  <section class="content-card mt-items-demo">
    <div class="table-header">
      <div>
        <h2 class="section-heading">{{ t('module_template.items.title') }}</h2>
        <p class="mt-items-demo__subtitle">{{ t('module_template.items.description') }}</p>
      </div>
      <div class="actions-wrapper">
        <button
          type="button"
          class="ui-btn ui-btn--primary"
          @click="openCreateModal"
        >
          <Plus :size="16" />
          <span>{{ t('module_template.items.create') }}</span>
        </button>
      </div>
    </div>

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
        <template #cell-attachment="{ item }">
          <button
            v-if="item.attachment_url"
            type="button"
            class="btn btn-link btn-sm p-0 d-inline-flex align-items-center gap-1"
            :aria-label="t('module_template.items.attachmentDownload')"
            @click="downloadAttachment(item)"
          >
            <Download :size="14" />
            <span>{{ item.attachment_name || t('module_template.items.attachment') }}</span>
          </button>
          <span v-else class="text-muted">—</span>
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
          <div class="actions-cell">
            <DropDown dropdown-menu-class="dropdown-menu-end" compact>
              <template #main>
                <button
                  type="button"
                  class="btn btn-link p-0"
                  :aria-label="t('module_template.items.actions')"
                >
                  <MoreHorizontal :size="18" />
                </button>
              </template>
              <template #list>
                <li>
                  <a
                    class="dropdown-item"
                    href="#"
                    @click.prevent="openEditModal(item)"
                  >
                    <Pencil :size="16" />
                    <span>{{ t('module_template.items.edit') }}</span>
                  </a>
                </li>
                <li>
                  <a
                    class="dropdown-item text-danger"
                    href="#"
                    @click.prevent="deleteItem(item)"
                  >
                    <Trash2 :size="16" />
                    <span>{{ t('module_template.items.delete') }}</span>
                  </a>
                </li>
              </template>
            </DropDown>
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
@import '../scss/page-shell.scss';

.mt-items-demo__subtitle {
  margin: 0.25rem 0 0;
  color: var(--ui-text-muted);
  font-size: 0.875rem;
  max-width: 36rem;
}

.mt-items-demo__toolbar {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  gap: 0.75rem;

  // SearchInput по умолчанию width: 100% — без этого фильтр уезжает на вторую строку
  :deep(.search-input) {
    flex: 1 1 0;
    min-width: 0;
    width: auto;
  }

  :deep(.select-box) {
    --select-box-font-size: 0.875rem;
  }
}

.mt-items-demo__filter {
  flex: 0 0 160px;
  width: 160px;
  min-width: 140px;
}

@media (max-width: 767.98px) {
  .mt-items-demo__toolbar {
    flex-wrap: wrap;

    :deep(.search-input) {
      flex: 1 1 100%;
      width: 100%;
    }
  }

  .mt-items-demo__filter {
    flex: 1 1 100%;
    width: 100%;
    min-width: 0;
  }
}
</style>
