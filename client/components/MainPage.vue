<template>
    <div class="mt-main-page">
        <div class="main-card">

            <!-- ───── Шапка ───── -->
            <div class="card-header">
                <div class="header-left">
                    <img :src="sdbLogo" alt="СКБ" class="module-logo" />
                    <div class="header-text">
                        <h1 class="module-title">Шаблон модуля</h1>
                        <p class="module-subtitle">
                            Учебный шаблон для разработки модулей в системе&nbsp;ERGO&nbsp;MS&nbsp;·&nbsp;СКБ
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
                        О шаблонном модуле
                    </h2>
                    <p class="welcome-description">
                        Модуль демонстрирует архитектурные соглашения ERGO MS: структуру API, работу с базой данных,
                        подключение очередей задач и интеграцию ML-сервисов. Используйте его как отправную точку для собственных модулей.
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
                        Мониторинг сервиса
                    </router-link>
                </div>

                <!-- ───── ML-демо ───── -->
                <div class="ml-demo">
                    <div class="ml-header">
                        <div class="ml-header-text">
                            <h2 class="section-heading mb-1">
                                <BrainCircuit :size="22" class="section-icon" />
                                Классификация текста
                            </h2>
                            <p class="welcome-description mb-0">
                                Rule-based ML-модель для разбора входящих обращений. Определяет категорию, приоритет и
                                ключевые признаки текста. Замените логику в&nbsp;<code>api/ml_service.py</code> на
                                настоящую модель, сохранив контракт&nbsp;API.
                            </p>
                        </div>
                        <span class="ml-badge">Rule-based ML</span>
                    </div>

                    <div class="row g-4 align-items-stretch">

                        <!-- Левая карточка: ввод -->
                        <div class="col-lg-5">
                            <div class="ml-card h-100">
                                <div class="ml-card-label">
                                    <FileText :size="14" />
                                    Входные данные
                                </div>

                                <div class="mb-3">
                                    <label class="form-label form-label-sm">Текст обращения</label>
                                    <textarea
                                        v-model="inputText"
                                        class="form-control form-control-sm"
                                        rows="5"
                                        placeholder="Введите текст или выберите пример ниже..."
                                        maxlength="2000"
                                    ></textarea>
                                    <div class="char-counter">{{ inputText.length }}&thinsp;/&thinsp;2000</div>
                                </div>

                                <div class="ml-examples mb-3">
                                    <span class="ml-examples-label">Примеры:</span>
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
                                    <span>{{ loadingPredict ? 'Классификация...' : 'Классифицировать' }}</span>
                                </button>
                            </div>
                        </div>

                        <!-- Правая карточка: результат -->
                        <div class="col-lg-7">
                            <div class="ml-card h-100">
                                <div class="ml-card-label">
                                    <BarChart2 :size="14" />
                                    Результат классификации
                                </div>

                                <!-- Метаданные модели -->
                                <div class="model-meta-row mb-3" v-if="modelMeta">
                                    <span class="model-meta-item">
                                        <span class="model-meta-key">Модель:</span>
                                        <span class="model-meta-val">{{ modelMeta.model_name }}</span>
                                    </span>
                                    <span class="model-meta-item">
                                        <span class="model-meta-key">Тип:</span>
                                        <span class="model-meta-val">{{ modelMeta.model_type }}</span>
                                    </span>
                                    <span class="model-meta-item">
                                        <span class="model-meta-key">Версия:</span>
                                        <span class="model-meta-val">{{ modelMeta.model_version }}</span>
                                    </span>
                                </div>
                                <div class="model-meta-row mb-3 text-muted small" v-else-if="loadingMeta">
                                    Загрузка метаданных модели...
                                </div>

                                <!-- Пустое состояние -->
                                <div class="ml-empty" v-if="!prediction && !loadingPredict">
                                    <BrainCircuit :size="32" class="ml-empty-icon" />
                                    <p>Результат появится после классификации</p>
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
                                            <span class="result-key">Категория</span>
                                            <span :class="['result-val', 'result-badge', `badge-cat--${prediction.category}`]">
                                                {{ categoryLabel(prediction.category) }}
                                            </span>
                                        </div>
                                        <div class="result-item">
                                            <span class="result-key">Приоритет</span>
                                            <span :class="['result-val', 'result-badge', `badge-pri--${prediction.priority}`]">
                                                {{ priorityLabel(prediction.priority) }}
                                            </span>
                                        </div>
                                        <div class="result-item">
                                            <span class="result-key">Балл важности</span>
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
                                            <span class="result-key">Символов / предложений</span>
                                            <span class="result-val">
                                                {{ prediction.text_length }}&thinsp;/&thinsp;{{ prediction.sentence_count }}
                                            </span>
                                        </div>
                                        <div class="result-item result-item--full" v-if="prediction.matched_keywords?.length">
                                            <span class="result-key">Сработавшие ключи</span>
                                            <div class="result-keywords">
                                                <span
                                                    v-for="kw in prediction.matched_keywords"
                                                    :key="kw"
                                                    class="kw-chip"
                                                >{{ kw }}</span>
                                            </div>
                                        </div>
                                        <div class="result-item result-item--full" v-if="prediction.note">
                                            <span class="result-key">Примечание</span>
                                            <span class="result-val text-muted">{{ prediction.note }}</span>
                                        </div>
                                    </div>

                                    <!-- Сырой JSON -->
                                    <details class="raw-json-details">
                                        <summary>Сырой ответ API</summary>
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
                        Как развивать этот модуль дальше
                    </h3>
                    <ul class="mt-howto-list">
                        <li class="mt-howto-item">
                            <span class="mt-howto-title">Подключите свою ML‑модель</span>
                            <span class="mt-howto-desc">
                                Замените rule‑based логику в <code>api/ml_service.py</code> на вызов обученной модели,
                                сохранив структуру ответа. Подробнее см. <code>HOWTO.md</code>.
                            </span>
                        </li>
                        <li class="mt-howto-item">
                            <span class="mt-howto-title">Добавьте реальные метрики мониторинга</span>
                            <span class="mt-howto-desc">
                                Расширьте <code>_demo_metrics()</code> в <code>api/views.py</code> и выведите новые поля
                                на <code>StatusPage.vue</code> через <code>useModuleTemplateStatus</code>.
                            </span>
                        </li>
                        <li class="mt-howto-item">
                            <span class="mt-howto-title">Создайте свою учебную страницу</span>
                            <span class="mt-howto-desc">
                                Добавьте компонент в <code>client/components</code>, маршрут в
                                <code>client/js/routes.js</code> и пункт меню в миграции API.
                            </span>
                        </li>
                    </ul>
                </div>

            </div>
        </div>
    </div>
</template>

<script setup>
import {
    Activity, Database, Layers, Code,
    BookOpen, GitBranch, GraduationCap,
    BrainCircuit, FileText, BarChart2, Lightbulb,
} from 'lucide-vue-next'

import sdbLogo from '../assets/svg/sdb.svg'
import { useModuleTemplateML } from '../js/useModuleTemplateML'

const {
    loadingMeta,
    loadingPredict,
    modelMeta,
    inputText,
    prediction,
    sendPredict,
} = useModuleTemplateML()

// ─── Фичи ───────────────────────────────────────────────────────────────────
const features = [
    {
        id: 'monitoring',
        icon: Activity,
        color: 'monitoring',
        title: 'Мониторинг доступности',
        tag: 'Health',
        desc: 'Health-check сервиса и подключения к БД с готовой страницей статуса.',
    },
    {
        id: 'data',
        icon: Database,
        color: 'db',
        title: 'Работа с данными',
        tag: 'Data',
        desc: 'Пример модели, миграций и роутера БД для студенческих проектов.',
    },
    {
        id: 'api',
        icon: Layers,
        color: 'api',
        title: 'REST API (DRF)',
        tag: 'API',
        desc: 'ViewSet-ы, сериализаторы и документация Swagger — образец академического API.',
    },
    {
        id: 'frontend',
        icon: Code,
        color: 'frontend',
        title: 'Vue-компоненты',
        tag: 'UI',
        desc: 'Composables, маршрутизация и SCSS-модули — шаблон фронтенд-модуля.',
    },
]

// ─── Примеры текстов ─────────────────────────────────────────────────────────
const examples = [
    {
        id: 'error',
        label: 'Ошибка',
        text: 'Критическая ошибка в production: сервис упал, логи показывают exception при запросе к БД. Срочно!',
    },
    {
        id: 'request',
        label: 'Запрос',
        text: 'Подскажите, пожалуйста, как получить доступ к аналитическому дашборду для нашего отдела.',
    },
    {
        id: 'report',
        label: 'Отчёт',
        text: 'Отчёт по продажам за 2025 год: динамика роста выручки составила 18% относительно прошлого периода.',
    },
    {
        id: 'task',
        label: 'Задача',
        text: 'Нужно разработать и добавить новый модуль экспорта данных в форматах CSV и XLSX.',
    },
]

const applyExample = (text) => {
    inputText.value = text
}

// ─── Вспомогательные функции ─────────────────────────────────────────────────
const CATEGORY_LABELS = {
    error: 'Ошибка',
    urgent: 'Срочно',
    request: 'Запрос',
    report: 'Отчёт',
    task: 'Задача',
    other: 'Другое',
}

const PRIORITY_LABELS = {
    high: 'Высокий',
    medium: 'Средний',
    low: 'Низкий',
}

const categoryLabel = (cat) => CATEGORY_LABELS[cat] ?? cat
const priorityLabel = (pri) => PRIORITY_LABELS[pri] ?? pri
</script>

<style lang="scss" scoped>
@import '../scss/main-page.scss';
</style>
