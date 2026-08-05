<template>
    <div class="mt-main-page">
        <div class="main-card">

            <!-- ───── Шапка ───── -->
            <div class="card-header">
                <div class="header-left">
                    <ContentImage
                        :src="sdbLogo"
                        :alt="t('module_template.logoAlt')"
                        class="module-logo"
                    />
                    <div class="header-text">
                        <h1 class="module-title">{{ t('module_template.title') }}</h1>
                        <p class="module-subtitle">
                            {{ t('module_template.subtitle') }}
                        </p>
                    </div>
                </div>
                <div class="header-meta">
                    <span class="meta-pill">
                        <BookOpen :size="13" />
                        module_template
                    </span>
                    <span class="meta-pill meta-pill--accent">
                        <GitBranch :size="13" />
                        v{{ systemVersion }}
                    </span>
                </div>
            </div>

            <div class="card-content">

                <!-- ───── Приветствие ───── -->
                <div class="welcome-section">
                    <h2 class="section-heading">
                        <GraduationCap :size="22" class="section-icon" />
                        {{ t('module_template.aboutHeading') }}
                    </h2>
                    <p class="welcome-description">
                        {{ t('module_template.aboutText') }}
                    </p>
                </div>

                <!-- ───── Фичи ───── -->
                <div class="features-grid">
                    <div class="feature-item" v-for="feat in features" :key="feat.id">
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

                <!-- ───── Кнопки перехода ───── -->
                <div class="action-section d-flex flex-wrap gap-2">
                    <router-link
                        :to="{ name: 'ModuleTemplateStatus' }"
                        class="btn btn-primary btn-sm d-inline-flex align-items-center gap-2"
                    >
                        <Activity :size="16" />
                        {{ t('module_template.monitorService') }}
                    </router-link>
                    <router-link
                        :to="{ name: 'ModuleTemplatePatterns' }"
                        class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center gap-2"
                    >
                        <BookOpen :size="16" />
                        {{ t('module_template.routes.patterns') }}
                    </router-link>
                </div>

                <!-- ───── ML-демо ───── -->
                <div class="ml-demo">
                    <div class="ml-header">
                        <div class="ml-header-text">
                            <h2 class="section-heading mb-1">
                                <BrainCircuit :size="22" class="section-icon" />
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
                                        class="btn btn-primary btn-sm d-inline-flex align-items-center gap-2"
                                        :disabled="loadingPredict || !inputText.trim()"
                                        @click="sendPredict"
                                    >
                                        <Activity :size="15" :class="{ spin: loadingPredict }" />
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
                                <div class="ml-result__title">
                                    <BarChart2 :size="16" />
                                    {{ t('module_template.ml.resultHeading') }}
                                </div>

                                <div v-if="modelMeta" class="model-meta-row mb-3">
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
                                <p v-else-if="loadingMeta" class="text-muted small mb-3">
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
                                            <span class="badge text-bg-primary">
                                                {{ categoryLabel(prediction.category) }}
                                            </span>
                                        </div>
                                        <div class="result-item">
                                            <span class="result-key">{{ t('module_template.ml.priority') }}</span>
                                            <span
                                                class="badge"
                                                :class="priorityBadgeClass(prediction.priority)"
                                            >
                                                {{ priorityLabel(prediction.priority) }}
                                            </span>
                                        </div>
                                        <div class="result-item">
                                            <span class="result-key">{{ t('module_template.ml.score') }}</span>
                                            <div class="result-score-wrap">
                                                <span class="result-score-num">{{ prediction.score }}</span>
                                                <div class="progress" role="progressbar" :aria-valuenow="prediction.score" aria-valuemin="0" aria-valuemax="100">
                                                    <div
                                                        class="progress-bar"
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
                                                    class="badge text-bg-secondary"
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
                                    <Lightbulb :size="13" aria-hidden="true" />
                                    {{ modelMeta.replace_hint }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ───── How-to блок ───── -->
                <div class="mt-howto mt-4">
                    <h3 class="section-heading mb-2">
                        <Lightbulb :size="18" class="section-icon" />
                        {{ t('module_template.howto.heading') }}
                    </h3>
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
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import {
    Activity, Database, Layers, Code,
    BookOpen, GitBranch, GraduationCap,
    BrainCircuit, BarChart2, Lightbulb,
} from 'lucide-vue-next'

import ContentImage from '@/components/ContentImage.vue'
import FormCard from '@/components/FormCard.vue'
import FormField from '@/components/FormField.vue'
import SelectBox from '@/components/SelectBox.vue'
import SpinnerLoading from '@/components/SpinnerLoading.vue'
import { useAppI18n } from '@/i18n/useAppI18n.js'
import { clientEnv } from '@/js/clientEnv.js'
import sdbLogo from '../assets/svg/sdb.svg'
import { useModuleTemplateML } from '../js/useModuleTemplateML'

const { t } = useAppI18n()
const systemVersion = clientEnv.systemVersion

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

const priorityBadgeClass = (pri) => {
    if (pri === 'high') return 'text-bg-danger'
    if (pri === 'medium') return 'text-bg-warning'
    return 'text-bg-secondary'
}
</script>

<style lang="scss" scoped>
@import '../scss/main-page.scss';

/* ContentImage: class попадает на img, размеры — на flex-обёртку */
.header-left :deep(.ergo-content-image) {
  width: 72px;
  height: 72px;
  flex-shrink: 0;
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
