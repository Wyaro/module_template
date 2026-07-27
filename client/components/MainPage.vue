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
                        v1.0
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

                <!-- ───── Кнопка перехода ───── -->
                <div class="action-section">
                    <router-link
                        :to="{ name: 'ModuleTemplateStatus' }"
                        class="btn btn-primary d-inline-flex align-items-center gap-2"
                    >
                        <Activity :size="16" />
                        {{ t('module_template.monitorService') }}
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
                        <span class="ml-badge">{{ t('module_template.ml.badge') }}</span>
                    </div>

                    <div class="row g-4 align-items-stretch">

                        <!-- Левая карточка: ввод -->
                        <div class="col-lg-5">
                            <div class="ml-card h-100">
                                <div class="ml-card-label">
                                    <FileText :size="14" />
                                    {{ t('module_template.ml.inputLabel') }}
                                </div>

                                <div class="mb-3">
                                    <label class="form-label form-label-sm">{{ t('module_template.ml.textLabel') }}</label>
                                    <textarea
                                        v-model="inputText"
                                        class="form-control form-control-sm"
                                        rows="5"
                                        :placeholder="t('module_template.ml.textPlaceholder')"
                                        maxlength="2000"
                                    ></textarea>
                                    <div class="char-counter">{{ inputText.length }}&thinsp;/&thinsp;2000</div>
                                </div>

                                <div class="ml-examples mb-3">
                                    <span class="ml-examples-label">{{ t('module_template.ml.examples') }}</span>
                                    <button
                                        v-for="ex in examples"
                                        :key="ex.id"
                                        type="button"
                                        class="btn btn-sm btn-outline-secondary ml-example-chip"
                                        @click="applyExample(ex.text)"
                                    >
                                        {{ ex.label }}
                                    </button>
                                </div>

                                <button
                                    class="btn btn-primary btn-sm d-inline-flex align-items-center gap-2"
                                    @click="sendPredict"
                                    :disabled="loadingPredict || !inputText.trim()"
                                >
                                    <Activity :size="15" :class="{ spin: loadingPredict }" />
                                    <span>{{ loadingPredict ? t('module_template.ml.classifying') : t('module_template.ml.classify') }}</span>
                                </button>
                            </div>
                        </div>

                        <!-- Правая карточка: результат -->
                        <div class="col-lg-7">
                            <div class="ml-card h-100">
                                <div class="ml-card-label">
                                    <BarChart2 :size="14" />
                                    {{ t('module_template.ml.resultHeading') }}
                                </div>

                                <!-- Метаданные модели -->
                                <div class="model-meta-row mb-3" v-if="modelMeta">
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
                                <div class="model-meta-row mb-3 text-muted small" v-else-if="loadingMeta">
                                    {{ t('module_template.ml.loadingMeta') }}
                                </div>

                                <!-- Пустое состояние -->
                                <div class="ml-empty" v-if="!prediction && !loadingPredict">
                                    <BrainCircuit :size="32" class="ml-empty-icon" />
                                    <p>{{ t('module_template.ml.emptyResult') }}</p>
                                </div>

                                <!-- Скелетон загрузки -->
                                <div class="ml-skeleton" v-else-if="loadingPredict">
                                    <div class="skeleton-line" style="width: 60%"></div>
                                    <div class="skeleton-line" style="width: 45%"></div>
                                    <div class="skeleton-line" style="width: 80%"></div>
                                </div>

                                <!-- Структурированный результат -->
                                <template v-else-if="prediction">
                                    <div class="result-grid">
                                        <div class="result-item">
                                            <span class="result-key">{{ t('module_template.ml.category') }}</span>
                                            <span :class="['result-val', 'result-badge', `badge-cat--${prediction.category}`]">
                                                {{ categoryLabel(prediction.category) }}
                                            </span>
                                        </div>
                                        <div class="result-item">
                                            <span class="result-key">{{ t('module_template.ml.priority') }}</span>
                                            <span :class="['result-val', 'result-badge', `badge-pri--${prediction.priority}`]">
                                                {{ priorityLabel(prediction.priority) }}
                                            </span>
                                        </div>
                                        <div class="result-item">
                                            <span class="result-key">{{ t('module_template.ml.score') }}</span>
                                            <div class="result-score-wrap">
                                                <span class="result-score-num">{{ prediction.score }}</span>
                                                <div class="score-bar-track">
                                                    <div
                                                        class="score-bar-fill"
                                                        :style="{ width: prediction.score + '%' }"
                                                    ></div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="result-item">
                                            <span class="result-key">{{ t('module_template.ml.charsSentences') }}</span>
                                            <span class="result-val">
                                                {{ prediction.text_length }}&thinsp;/&thinsp;{{ prediction.sentence_count }}
                                            </span>
                                        </div>
                                        <div class="result-item result-item--full" v-if="prediction.matched_keywords?.length">
                                            <span class="result-key">{{ t('module_template.ml.matchedKeys') }}</span>
                                            <div class="result-keywords">
                                                <span
                                                    v-for="kw in prediction.matched_keywords"
                                                    :key="kw"
                                                    class="kw-chip"
                                                >{{ kw }}</span>
                                            </div>
                                        </div>
                                        <div class="result-item result-item--full" v-if="prediction.note">
                                            <span class="result-key">{{ t('module_template.ml.note') }}</span>
                                            <span class="result-val text-muted">{{ prediction.note }}</span>
                                        </div>
                                    </div>

                                    <!-- Сырой JSON -->
                                    <details class="raw-json-details">
                                        <summary>{{ t('module_template.ml.rawResponse') }}</summary>
                                        <pre class="raw-json">{{ JSON.stringify(prediction, null, 2) }}</pre>
                                    </details>
                                </template>

                                <!-- Подсказка для студентов -->
                                <div class="ml-hint" v-if="modelMeta?.replace_hint">
                                    <Lightbulb :size="13" />
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
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import {
    Activity, Database, Layers, Code,
    BookOpen, GitBranch, GraduationCap,
    BrainCircuit, FileText, BarChart2, Lightbulb,
} from 'lucide-vue-next'

import ContentImage from '@/components/ContentImage.vue'
import sdbLogo from '../assets/svg/sdb.svg'
import { useModuleTemplateML } from '../js/useModuleTemplateML'

const { t } = useI18n()

const {
    loadingMeta,
    loadingPredict,
    modelMeta,
    inputText,
    prediction,
    sendPredict,
} = useModuleTemplateML()

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
        text: 'Критическая ошибка в production: сервис упал, логи показывают exception при запросе к БД. Срочно!',
    },
    {
        id: 'request',
        label: t('module_template.ml.exampleRequest'),
        text: 'Подскажите, пожалуйста, как получить доступ к аналитическому дашборду для нашего отдела.',
    },
    {
        id: 'report',
        label: t('module_template.ml.exampleReport'),
        text: 'Отчёт по продажам за 2025 год: динамика роста выручки составила 18% относительно прошлого периода.',
    },
    {
        id: 'task',
        label: t('module_template.ml.exampleTask'),
        text: 'Нужно разработать и добавить новый модуль экспорта данных в форматах CSV и XLSX.',
    },
])

const applyExample = (text) => {
    inputText.value = text
}

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
</script>

<style lang="scss" scoped>
@import '../scss/main-page.scss';

/* ContentImage: class попадает на img, размеры — на flex-обёртку */
.header-left :deep(.ergo-content-image) {
  width: 72px;
  height: 72px;
  flex-shrink: 0;
}
</style>
