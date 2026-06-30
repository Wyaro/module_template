import { ref, onMounted } from 'vue'
import { apiClient } from '@/js/api/manager'
import { useToast } from '@/js/utils/toast.js'

import { moduleTemplateEndpoints } from './endpoints'

const MAX_INPUT_LENGTH = 2000

export function useModuleTemplateML() {
  const toast = useToast()

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
        toast.warning(response.message || 'Не удалось получить информацию о модели')
      }
    } catch {
      toast.error('Ошибка при получении информации о модели')
    } finally {
      loadingMeta.value = false
    }
  }

  const sendPredict = async () => {
    const text = inputText.value.trim()
    if (!text) {
      toast.info('Введите текст для классификации')
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
        toast.success('Классификация выполнена')
      } else {
        toast.warning(response.message || 'Не удалось получить предсказание')
      }
    } catch {
      toast.error('Ошибка при обращении к ML-сервису')
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
