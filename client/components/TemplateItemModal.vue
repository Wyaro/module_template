<script setup>
import { computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import ModalCenter from '@/components/ModalCenter.vue'
import { apiClient } from '@/js/api/manager'
import { extractApiError } from '@/js/utils/apiErrorMessage.js'
import { logError } from '@/js/utils/logError.js'
import { useToast } from '@/js/utils/toast.js'

import { moduleTemplateEndpoints } from '../js/endpoints'

const props = defineProps({
  visible: { type: Boolean, default: false },
  item: { type: Object, default: null },
})

const emit = defineEmits(['close', 'saved'])

const { t } = useI18n()
const toast = useToast()

const formId = 'template-item-form'
const name = ref('')
const description = ref('')
const active = ref(true)
const error = ref('')
const isSubmitting = ref(false)

const isEdit = computed(() => Boolean(props.item?.public_id))
const modalTitle = computed(() =>
  isEdit.value
    ? t('module_template.items.editTitle')
    : t('module_template.items.createTitle'),
)

const itemsUrl = moduleTemplateEndpoints.moduleTemplate.items

const resetForm = () => {
  name.value = props.item?.name || ''
  description.value = props.item?.description || ''
  active.value = props.item?.active ?? true
  error.value = ''
}

watch(
  () => props.visible,
  (isOpen) => {
    if (isOpen) {
      resetForm()
    }
  },
  { immediate: true },
)

const close = () => {
  if (isSubmitting.value) {
    return
  }
  emit('close')
}

const submit = async () => {
  error.value = ''
  if (!name.value.trim()) {
    error.value = t('module_template.items.nameRequired')
    return
  }

  isSubmitting.value = true
  const payload = {
    name: name.value.trim(),
    description: description.value.trim(),
    active: active.value,
  }

  try {
    let response
    if (isEdit.value) {
      response = await apiClient.put(`${itemsUrl}${props.item.public_id}/`, payload)
    } else {
      response = await apiClient.post(itemsUrl, payload)
    }

    if (!response.success) {
      error.value = response.message || t('module_template.items.saveFail')
      return
    }

    toast.success(
      isEdit.value
        ? t('module_template.items.updateSuccess')
        : t('module_template.items.createSuccess'),
    )
    emit('saved')
  } catch (apiError) {
    logError('TemplateItemModal.submit', apiError)
    error.value = extractApiError(apiError, t('module_template.items.saveError'))
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <ModalCenter
    standalone
    modal-id="templateItemModal"
    :title="modalTitle"
    size="md"
    :visible="visible"
    :close-on-esc="!isSubmitting"
    @close="close"
  >
    <form :id="formId" class="template-item-modal" @submit.prevent="submit">
      <div class="mb-3">
        <label class="form-label" for="template-item-name">
          {{ t('module_template.items.name') }}
        </label>
        <input
          id="template-item-name"
          v-model="name"
          type="text"
          class="form-control"
          maxlength="255"
          required
        />
      </div>
      <div class="mb-3">
        <label class="form-label" for="template-item-description">
          {{ t('module_template.items.descriptionCol') }}
        </label>
        <textarea
          id="template-item-description"
          v-model="description"
          class="form-control"
          rows="3"
        />
      </div>
      <div class="form-check">
        <input
          id="template-item-active"
          v-model="active"
          class="form-check-input"
          type="checkbox"
        />
        <label class="form-check-label" for="template-item-active">
          {{ t('module_template.items.active') }}
        </label>
      </div>
      <p v-if="error" class="text-danger small mt-3 mb-0">{{ error }}</p>
    </form>

    <template #footer>
      <button
        type="button"
        class="btn btn-outline-secondary"
        :disabled="isSubmitting"
        @click="close"
      >
        {{ t('module_template.items.cancel') }}
      </button>
      <button
        type="submit"
        :form="formId"
        class="btn btn-primary"
        :disabled="isSubmitting"
      >
        {{ isSubmitting ? t('module_template.loading') : t('module_template.items.save') }}
      </button>
    </template>
  </ModalCenter>
</template>
