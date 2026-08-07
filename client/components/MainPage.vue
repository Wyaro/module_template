<template>
  <div class="admin-page mt-main-page">
    <div class="page-header">
      <div class="mt-main-page__brand">
        <span class="module-mark" :aria-label="t('module_template.logoAlt')" role="img">
          <!-- Макет модуля: рамка + колонка + строки — как LayoutTemplate Lucide, stroke как ErgomsLogo -->
          <svg
            class="module-mark__svg"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <rect
              x="3"
              y="3"
              width="18"
              height="18"
              rx="3"
              stroke="currentColor"
              stroke-width="2"
            />
            <path d="M9 3v18" stroke="currentColor" stroke-width="2" />
            <path
              d="M13 8h5M13 12h5M13 16h3.5"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </span>
        <div class="mt-main-page__brand-text">
          <h1 class="page-title">{{ t('module_template.title') }}</h1>
          <p class="page-subtitle">{{ t('module_template.subtitle') }}</p>
          <p class="page-header__meta">
            module_template · v{{ systemVersion }}
          </p>
        </div>
      </div>
      <div class="page-header__actions actions-wrapper">
        <button
          type="button"
          class="ui-btn ui-btn--primary"
          @click="goToStatus"
        >
          <Activity :size="16" aria-hidden="true" />
          <span>{{ t('module_template.monitorService') }}</span>
        </button>
        <button
          type="button"
          class="ui-btn ui-btn--secondary"
          @click="goToPatterns"
        >
          <BookOpen :size="16" aria-hidden="true" />
          <span>{{ t('module_template.routes.patterns') }}</span>
        </button>
      </div>
    </div>

    <div class="content-card">
      <h2 class="section-heading">
        <GraduationCap :size="18" class="section-heading__icon" />
        {{ t('module_template.aboutHeading') }}
      </h2>
      <p class="welcome-description">
        {{ t('module_template.aboutText') }}
      </p>

      <div class="features-grid">
        <div v-for="feat in features" :key="feat.id" class="feature-item">
          <div :class="['feature-icon', `feature-icon--${feat.color}`]">
            <component :is="feat.icon" :size="18" />
          </div>
          <div class="feature-text">
            <div class="feature-title-row">
              <span class="feature-title">{{ feat.title }}</span>
              <span class="feature-tag">{{ feat.tag }}</span>
            </div>
            <span class="feature-desc">{{ feat.desc }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="content-card">
      <div class="ml-header">
        <div class="ml-header-text">
          <h2 class="section-heading mb-1">
            <BrainCircuit :size="18" class="section-heading__icon" />
            {{ t('module_template.ml.heading') }}
          </h2>
          <p class="welcome-description mb-0">
            {{ t('module_template.ml.description') }}
          </p>
        </div>
        <span class="badge text-bg-secondary">{{ t('module_template.ml.badge') }}</span>
      </div>

      <div class="row g-3 align-items-stretch">
        <div class="col-lg-5">
          <FormCard class="h-100">
            <FormField
              :label="t('module_template.ml.textLabel')"
              label-for="mt-ml-text"
            >
              <textarea
                id="mt-ml-text"
                v-model="inputText"
                class="form-control form-control-sm"
                rows="5"
                :placeholder="t('module_template.ml.textPlaceholder')"
                maxlength="2000"
              />
              <div class="char-counter">{{ inputText.length }}&thinsp;/&thinsp;2000</div>
            </FormField>
            <FormField
              :label="t('module_template.ml.examples')"
              label-for="mt-ml-example"
              last
            >
              <SelectBox
                id="mt-ml-example"
                v-model="selectedExampleId"
                :options="examples"
                value-key="id"
                label-key="label"
                :include-all-option="true"
                :all-label="t('module_template.ml.examplesPlaceholder')"
              />
            </FormField>
            <template #footer>
              <button
                type="button"
                class="ui-btn ui-btn--primary"
                :disabled="loadingPredict || !inputText.trim()"
                @click="sendPredict"
              >
                <Activity :size="16" :class="{ spin: loadingPredict }" />
                <span>
                  {{ loadingPredict
                    ? t('module_template.ml.classifying')
                    : t('module_template.ml.classify') }}
                </span>
              </button>
            </template>
          </FormCard>
        </div>

        <div class="col-lg-7">
          <div class="ml-result h-100">
            <h3 class="section-heading ml-result__title">
              <BarChart2 :size="16" class="section-heading__icon" />
              {{ t('module_template.ml.resultHeading') }}
            </h3>

            <div v-if="modelMeta" class="model-meta-row">
              <span class="model-meta-item">
                <span class="model-meta-key">{{ t('module_template.ml.model') }}:</span>
                <span class="model-meta-val">{{ modelMeta.model_name }}</span>
              </span>
              <span class="model-meta-item">
                <span class="model-meta-key">{{ t('module_template.ml.type') }}:</span>
                <span class="model-meta-val">{{ modelMeta.model_type }}</span>
              </span>
              <span class="model-meta-item">
                <span class="model-meta-key">{{ t('module_template.ml.version') }}:</span>
                <span class="model-meta-val">{{ modelMeta.model_version }}</span>
              </span>
            </div>
            <p v-else-if="loadingMeta" class="text-muted small mb-0">
              {{ t('module_template.ml.loadingMeta') }}
            </p>

            <div v-if="loadingPredict" class="ml-result__loading">
              <SpinnerLoading />
            </div>

            <div v-else-if="!prediction" class="ml-empty">
              <BrainCircuit :size="28" class="ml-empty-icon" aria-hidden="true" />
              <p class="mb-0">{{ t('module_template.ml.emptyResult') }}</p>
            </div>

            <template v-else>
              <div class="result-grid">
                <div class="result-item">
                  <span class="result-key">{{ t('module_template.ml.category') }}</span>
                  <span class="ml-chip ml-chip--accent">
                    {{ categoryLabel(prediction.category) }}
                  </span>
                </div>
                <div class="result-item">
                  <span class="result-key">{{ t('module_template.ml.priority') }}</span>
                  <span
                    class="ml-chip"
                    :class="priorityChipClass(prediction.priority)"
                  >
                    {{ priorityLabel(prediction.priority) }}
                  </span>
                </div>
                <div class="result-item">
                  <span class="result-key">{{ t('module_template.ml.score') }}</span>
                  <div class="result-score-wrap">
                    <span class="result-score-num">{{ prediction.score }}</span>
                    <div
                      class="result-score-bar"
                      role="progressbar"
                      :aria-valuenow="prediction.score"
                      aria-valuemin="0"
                      aria-valuemax="100"
                    >
                      <div
                        class="result-score-bar__fill"
                        :style="{ width: prediction.score + '%' }"
                      />
                    </div>
                  </div>
                </div>
                <div class="result-item">
                  <span class="result-key">{{ t('module_template.ml.charsSentences') }}</span>
                  <span class="result-val">
                    {{ prediction.text_length }}&thinsp;/&thinsp;{{ prediction.sentence_count }}
                  </span>
                </div>
                <div
                  v-if="prediction.matched_keywords?.length"
                  class="result-item result-item--full"
                >
                  <span class="result-key">{{ t('module_template.ml.matchedKeys') }}</span>
                  <div class="result-keywords">
                    <span
                      v-for="kw in prediction.matched_keywords"
                      :key="kw"
                      class="ml-chip ml-chip--muted"
                    >{{ kw }}</span>
                  </div>
                </div>
                <div
                  v-if="prediction.note"
                  class="result-item result-item--full"
                >
                  <span class="result-key">{{ t('module_template.ml.note') }}</span>
                  <span class="result-val text-muted">{{ prediction.note }}</span>
                </div>
              </div>

              <details class="raw-json-details">
                <summary>{{ t('module_template.ml.rawResponse') }}</summary>
                <pre class="raw-json">{{ JSON.stringify(prediction, null, 2) }}</pre>
              </details>
            </template>

            <div v-if="modelMeta?.replace_hint" class="ml-hint">
              <Lightbulb :size="14" class="ml-hint__icon" aria-hidden="true" />
              <span>{{ modelMeta.replace_hint }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="content-card">
      <h2 class="section-heading">
        <Lightbulb :size="18" class="section-heading__icon" />
        {{ t('module_template.howto.heading') }}
      </h2>
      <ul class="mt-howto-list">
        <li class="mt-howto-item">
          <span class="mt-howto-title">{{ t('module_template.howto.mlTitle') }}</span>
          <span class="mt-howto-desc">{{ t('module_template.howto.mlDesc') }}</span>
        </li>
        <li class="mt-howto-item">
          <span class="mt-howto-title">{{ t('module_template.howto.metricsTitle') }}</span>
          <span class="mt-howto-desc">{{ t('module_template.howto.metricsDesc') }}</span>
        </li>
        <li class="mt-howto-item">
          <span class="mt-howto-title">{{ t('module_template.howto.pageTitle') }}</span>
          <span class="mt-howto-desc">{{ t('module_template.howto.pageDesc') }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  Activity, Database, Layers, Code,
  BookOpen, GraduationCap,
  BrainCircuit, BarChart2, Lightbulb,
} from 'lucide-vue-next'

import FormCard from '@/components/FormCard.vue'
import FormField from '@/components/FormField.vue'
import SelectBox from '@/components/SelectBox.vue'
import SpinnerLoading from '@/components/SpinnerLoading.vue'
import { useAppI18n } from '@/i18n/useAppI18n.js'
import { clientEnv } from '@/js/clientEnv.js'
import { useModuleTemplateML } from '../js/useModuleTemplateML'

const { t } = useAppI18n()
const router = useRouter()
const systemVersion = clientEnv.systemVersion

const goToStatus = () => {
  router.push({ name: 'ModuleTemplateStatus' })
}

const goToPatterns = () => {
  router.push({ name: 'ModuleTemplatePatterns' })
}

const {
  loadingMeta,
  loadingPredict,
  modelMeta,
  inputText,
  prediction,
  sendPredict,
} = useModuleTemplateML()

const selectedExampleId = ref('')

const features = computed(() => [
  {
    id: 'monitoring',
    icon: Activity,
    color: 'monitoring',
    title: t('module_template.features.monitoring.title'),
    tag: t('module_template.features.monitoring.tag'),
    desc: t('module_template.features.monitoring.desc'),
  },
  {
    id: 'data',
    icon: Database,
    color: 'db',
    title: t('module_template.features.data.title'),
    tag: t('module_template.features.data.tag'),
    desc: t('module_template.features.data.desc'),
  },
  {
    id: 'api',
    icon: Layers,
    color: 'api',
    title: t('module_template.features.api.title'),
    tag: t('module_template.features.api.tag'),
    desc: t('module_template.features.api.desc'),
  },
  {
    id: 'frontend',
    icon: Code,
    color: 'frontend',
    title: t('module_template.features.frontend.title'),
    tag: t('module_template.features.frontend.tag'),
    desc: t('module_template.features.frontend.desc'),
  },
])

const examples = computed(() => [
  {
    id: 'error',
    label: t('module_template.ml.exampleError'),
    text: t('module_template.ml.exampleErrorText'),
  },
  {
    id: 'request',
    label: t('module_template.ml.exampleRequest'),
    text: t('module_template.ml.exampleRequestText'),
  },
  {
    id: 'report',
    label: t('module_template.ml.exampleReport'),
    text: t('module_template.ml.exampleReportText'),
  },
  {
    id: 'task',
    label: t('module_template.ml.exampleTask'),
    text: t('module_template.ml.exampleTaskText'),
  },
])

watch(selectedExampleId, (id) => {
  if (!id) {
    return
  }
  const example = examples.value.find((item) => item.id === id)
  if (example) {
    inputText.value = example.text
  }
})

const categoryLabel = (cat) => {
  const key = `module_template.ml.categories.${cat}`
  const label = t(key)
  return label === key ? cat : label
}

const priorityLabel = (pri) => {
  const key = `module_template.ml.priorities.${pri}`
  const label = t(key)
  return label === key ? pri : label
}

const priorityChipClass = (pri) => {
  if (pri === 'high') return 'ml-chip--danger'
  if (pri === 'medium') return 'ml-chip--warning'
  return 'ml-chip--muted'
}
</script>

<style lang="scss" scoped>
@import '../scss/page-shell.scss';
@import '../scss/main-page.scss';

.mt-main-page__brand {
  display: flex;
  align-items: flex-start;
  gap: 0.875rem;
}

.mt-main-page__brand-text {
  min-width: 0;
}

.module-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  margin-top: 0.1rem;
  flex-shrink: 0;
  border-radius: var(--ui-radius);
  background: var(--ui-accent-soft);
  color: var(--color-accent, var(--ui-accent));
}

.module-mark__svg {
  width: 22px;
  height: 22px;
  display: block;
}

.col-lg-5 :deep(.form-card) {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.col-lg-5 :deep(.form-card__body) {
  flex: 1 1 auto;
}

.col-lg-5 :deep(.select-box) {
  --select-box-font-size: 0.875rem;
}
</style>
