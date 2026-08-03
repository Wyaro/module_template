import { ref, onMounted } from 'vue'
import { useAppI18n } from '@/i18n/useAppI18n.js'
import { apiClient } from '@/js/api/manager'
import { useToast } from '@/js/utils/toast.js'
import { logError } from '@/js/utils/logError.js'

import { moduleTemplateEndpoints } from './endpoints'

const MAX_INPUT_LENGTH = 2000

export function useModuleTemplateML() {
  const toast = useToast()
  const { t } = useAppI18n()

  const loadingMeta = ref(false)
  const loadingPredict = ref(false)

  const modelMeta = ref(null)
  const inputText = ref('')
  const prediction = ref(null)

  const fetchMeta = async () => {
    loadingMeta.value = true
    try {
      const response = await apiClient.get(moduleTemplateEndpoints.moduleTemplate.ml.meta)
      if (response.success) {
        modelMeta.value = response.data
      } else {
        toast.warning(response.message || t('module_template.ml.toast.metaFail'))
      }
    } catch (error) {
      logError('useModuleTemplateML.fetchMeta', error)
      toast.error(t('module_template.ml.toast.metaError'))
    } finally {
      loadingMeta.value = false
    }
  }

  const sendPredict = async () => {
    const text = inputText.value.trim()
    if (!text) {
      toast.info(t('module_template.ml.toast.enterText'))
      return
    }

    loadingPredict.value = true
    prediction.value = null

    try {
      const response = await apiClient.post(
        moduleTemplateEndpoints.moduleTemplate.ml.predict,
        { text: text.slice(0, MAX_INPUT_LENGTH) },
      )

      if (response.success) {
        prediction.value = response.data
        toast.success(t('module_template.ml.toast.success'))
      } else {
        toast.warning(response.message || t('module_template.ml.toast.predictFail'))
      }
    } catch (error) {
      logError('useModuleTemplateML.sendPredict', error)
      toast.error(t('module_template.ml.toast.predictError'))
    } finally {
      loadingPredict.value = false
    }
  }

  onMounted(() => {
    fetchMeta()
  })

  return {
    loadingMeta,
    loadingPredict,
    modelMeta,
    inputText,
    prediction,
    fetchMeta,
    sendPredict,
  }
}
