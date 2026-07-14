<template>
    <div class="mt-status-page">

        <!-- Header -->
        <div class="mt-header">
            <div class="mt-header-left">
                <div class="mt-header-icon">
                    <Activity :size="20" />
                </div>
                <div class="mt-header-text">
                    <h1 class="mt-page-title">Мониторинг шаблонного модуля</h1>
                    <p class="mt-page-subtitle">
                        Учебная панель мониторинга для примера health‑check и базовых метрик производительности.
                    </p>
                    <p class="mt-last-updated">
                        Последнее обновление:
                        <strong>{{ formatTime(lastUpdated || statusData.time) }}</strong>
                    </p>
                </div>
            </div>
            <div class="mt-controls">
                <span class="mt-monitoring-badge">Monitoring demo</span>
                <div class="mt-controls-row">
                    <div class="form-check form-switch mb-0">
                        <input
                            class="form-check-input"
                            type="checkbox"
                            id="mt-auto-refresh"
                            v-model="autoRefreshEnabled"
                            @change="setupAutoRefresh"
                        />
                        <label class="form-check-label small" for="mt-auto-refresh">
                            Авто {{ autoRefreshSeconds }}с
                        </label>
                    </div>
                    <button
                        class="btn btn-sm btn-primary d-flex align-items-center gap-1"
                        @click="refreshStatus"
                        :disabled="loading"
                    >
                        <RefreshCw :size="14" :class="{ spin: loading }" />
                        Обновить
                    </button>
                </div>
            </div>
        </div>

        <!-- Status cards -->
        <div class="row g-3 mb-4">
            <div class="col-sm-6 col-xl-3">
                <div class="mt-card" :class="`mt-card--${statusData.status === 'ok' ? 'ok' : 'fail'}`">
                    <div class="mt-card-icon">
                        <CheckCircle v-if="statusData.status === 'ok'" :size="20" />
                        <XCircle v-else :size="20" />
                    </div>
                    <div class="mt-card-body">
                        <span class="mt-card-label">Сервис</span>
                        <span class="mt-card-value">
                            {{ statusData.status === 'ok' ? 'Работает' : 'Ошибка' }}
                        </span>
                    </div>
                    <span class="mt-badge" :class="`mt-badge--${statusData.status === 'ok' ? 'ok' : 'fail'}`">
                        {{ statusData.status === 'ok' ? 'OK' : 'FAIL' }}
                    </span>
                </div>
            </div>

            <div class="col-sm-6 col-xl-3">
                <div class="mt-card" :class="`mt-card--${statusData.db === 'ok' ? 'ok' : 'fail'}`">
                    <div class="mt-card-icon">
                        <Database :size="20" />
                    </div>
                    <div class="mt-card-body">
                        <span class="mt-card-label">База данных</span>
                        <span class="mt-card-value">
                            {{ statusData.db === 'ok' ? 'Подключена' : 'Недоступна' }}
                        </span>
                    </div>
                    <span class="mt-badge" :class="`mt-badge--${statusData.db === 'ok' ? 'ok' : 'fail'}`">
                        {{ statusData.db === 'ok' ? 'OK' : 'FAIL' }}
                    </span>
                </div>
            </div>

            <div class="col-sm-6 col-xl-3">
                <div class="mt-card mt-card--neutral">
                    <div class="mt-card-icon">
                        <Clock :size="20" />
                    </div>
                    <div class="mt-card-body">
                        <span class="mt-card-label">Время работы</span>
                        <span class="mt-card-value">{{ formatUptime(statusData.uptime_seconds) }}</span>
                    </div>
                    <span class="mt-badge mt-badge--info">{{ statusData.environment }}</span>
                </div>
            </div>

            <div class="col-sm-6 col-xl-3">
                <div class="mt-card mt-card--neutral">
                    <div class="mt-card-icon">
                        <Server :size="20" />
                    </div>
                    <div class="mt-card-body">
                        <span class="mt-card-label">Узел / версия</span>
                        <span class="mt-card-value">{{ statusData.node_name }}</span>
                    </div>
                    <span class="mt-badge mt-badge--neutral">v{{ statusData.app_version }}</span>
                </div>
            </div>
        </div>

        <!-- Metric cards -->
        <div class="row g-3 mb-4">
            <div class="col-md-4">
                <div class="mt-metric-card" :class="`mt-metric-card--${latencyLevel}`">
                    <div class="mt-metric-header">
                        <Activity :size="16" />
                        <span>Задержка ответа</span>
                        <span class="mt-badge ms-auto" :class="`mt-badge--${latencyLevel}`">
                            {{ latencyLevel.toUpperCase() }}
                        </span>
                    </div>
                    <div class="mt-metric-value">
                        {{ statusData.latency_ms != null ? `${statusData.latency_ms} мс` : '—' }}
                    </div>
                    <div class="mt-metric-bar">
                        <div
                            class="mt-metric-bar-fill"
                            :class="`mt-metric-bar-fill--${latencyLevel}`"
                            :style="{ width: `${Math.min(100, ((statusData.latency_ms ?? 0) / 200) * 100)}%` }"
                        ></div>
                    </div>
                    <div class="mt-metric-aggregates" v-if="metricAggregates.latencyAvg != null">
                        <span>ср {{ metricAggregates.latencyAvg }} мс</span>
                        <span>мин {{ metricAggregates.latencyMin }} мс</span>
                        <span>макс {{ metricAggregates.latencyMax }} мс</span>
                    </div>
                    <p class="mt-metric-hint">Уровни для примера: warn &gt; 80 мс, crit &gt; 150 мс</p>
                </div>
            </div>

            <div class="col-md-4">
                <div class="mt-metric-card" :class="`mt-metric-card--${rpsLevel}`">
                    <div class="mt-metric-header">
                        <Zap :size="16" />
                        <span>Запросов в минуту</span>
                        <span class="mt-badge ms-auto" :class="`mt-badge--${rpsLevel}`">
                            {{ rpsLevel.toUpperCase() }}
                        </span>
                    </div>
                    <div class="mt-metric-value">
                        {{ statusData.requests_per_minute != null ? statusData.requests_per_minute : '—' }}
                    </div>
                    <div class="mt-metric-bar">
                        <div
                            class="mt-metric-bar-fill"
                            :class="`mt-metric-bar-fill--${rpsLevel}`"
                            :style="{ width: `${Math.min(100, ((statusData.requests_per_minute ?? 0) / 100) * 100)}%` }"
                        ></div>
                    </div>
                    <div class="mt-metric-aggregates" v-if="metricAggregates.rpsAvg != null">
                        <span>ср {{ metricAggregates.rpsAvg }} RPS</span>
                    </div>
                    <p class="mt-metric-hint">Учебные пороги нагрузки: warn &gt; 50, crit &gt; 80 RPS</p>
                </div>
            </div>

            <div class="col-md-4">
                <div class="mt-metric-card" :class="`mt-metric-card--${errorRateLevel}`">
                    <div class="mt-metric-header">
                        <AlertTriangle :size="16" />
                        <span>Процент ошибок</span>
                        <span class="mt-badge ms-auto" :class="`mt-badge--${errorRateLevel}`">
                            {{ errorRateLevel.toUpperCase() }}
                        </span>
                    </div>
                    <div class="mt-metric-value">
                        {{ statusData.error_rate != null ? `${statusData.error_rate}%` : '—' }}
                    </div>
                    <div class="mt-metric-bar">
                        <div
                            class="mt-metric-bar-fill"
                            :class="`mt-metric-bar-fill--${errorRateLevel}`"
                            :style="{ width: `${Math.min(100, ((statusData.error_rate ?? 0) / 10) * 100)}%` }"
                        ></div>
                    </div>
                    <div class="mt-metric-aggregates" v-if="metricAggregates.errorRateAvg != null">
                        <span>ср {{ metricAggregates.errorRateAvg }}%</span>
                    </div>
                    <p class="mt-metric-hint">Учебные пороги отказов: warn &gt; 2%, crit &gt; 5%</p>
                </div>
            </div>
        </div>

        <!-- Charts -->
        <div class="row g-3 mb-4">
            <div class="col-lg-8">
                <div class="card border-0 h-100 mt-chart-card">
                    <div class="card-body">
                        <h6 class="mt-chart-title">
                            <TrendingUp :size="15" />
                            Задержка ответа — история
                            <span class="text-muted fw-normal ms-1 small">(демо)</span>
                        </h6>
                        <p class="mt-chart-subtitle">
                            Временная динамика задержки последнего запроса к health‑check (чем ниже кривая, тем лучше).
                        </p>

                        <div v-if="latencyChart.path" class="mt-line-chart">
                            <svg
                                viewBox="0 0 300 64"
                                preserveAspectRatio="none"
                                width="100%"
                                height="80"
                            >
                                <defs>
                                    <linearGradient id="mt-latency-grad" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="0%"   style="stop-color: var(--bs-primary); stop-opacity: 0.2" />
                                        <stop offset="100%" style="stop-color: var(--bs-primary); stop-opacity: 0" />
                                    </linearGradient>
                                </defs>
                                <path :d="latencyChart.area" fill="url(#mt-latency-grad)" />
                                <path
                                    :d="latencyChart.path"
                                    fill="none"
                                    :style="{ stroke: 'var(--bs-primary)', strokeWidth: '1.5', strokeLinejoin: 'round' }"
                                />
                                <circle
                                    v-if="latencyChart.dots.length"
                                    :cx="latencyChart.dots[latencyChart.dots.length - 1].x"
                                    :cy="latencyChart.dots[latencyChart.dots.length - 1].y"
                                    r="3"
                                    :style="{ fill: 'var(--bs-primary)' }"
                                />
                            </svg>
                            <div class="mt-chart-labels">
                                <span>{{ formatShortTime(history[history.length - 1]?.time) }}</span>
                                <span>{{ formatShortTime(history[0]?.time) }}</span>
                            </div>
                        </div>
                        <div v-else class="mt-chart-empty">
                            Данные появятся после нескольких обновлений health‑check.
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-4">
                <div class="card border-0 h-100 mt-chart-card">
                    <div class="card-body">
                        <h6 class="mt-chart-title">
                            <BarChart2 :size="15" />
                            Запросы в минуту
                            <span class="text-muted fw-normal ms-1 small">(демо)</span>
                        </h6>
                        <p class="mt-chart-subtitle">
                            Оценка интенсивности нагрузки по числу запросов в минуту за последние измерения.
                        </p>

                        <div v-if="rpsBars.length" class="mt-bar-chart">
                            <div
                                v-for="(bar, i) in rpsBars"
                                :key="i"
                                class="mt-bar"
                                :class="`mt-bar--${bar.level}`"
                                :style="{ height: `${bar.height}%` }"
                                :title="`${bar.rps} RPS`"
                            ></div>
                        </div>
                        <div v-else class="mt-chart-empty">
                            Данные появятся после нескольких обновлений health‑check.
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- History log -->
        <div class="card border-0 mb-4 mt-chart-card">
            <div class="card-header bg-transparent border-0 pt-3 pb-2 d-flex align-items-center justify-content-between">
                <h6 class="mb-0 d-flex align-items-center gap-2">
                    <List :size="16" />
                    Журнал измерений
                </h6>
                <span class="text-muted small">{{ history.length }} из {{ HISTORY_LIMIT }}</span>
            </div>
            <div class="card-body pt-1">
                <div v-if="!history.length" class="text-muted small py-2">
                    Журнал появится после первого обновления health‑check.
                </div>
                <div v-else class="mt-history-log">
                    <div
                        v-for="(item, i) in history"
                        :key="i"
                        class="mt-log-row"
                        :class="{
                            'mt-log-row--ok':   item.status === 'ok' && item.db === 'ok',
                            'mt-log-row--warn': item.status === 'ok' && item.db !== 'ok',
                            'mt-log-row--fail': item.status !== 'ok',
                        }"
                    >
                        <div class="mt-log-dot"></div>
                        <span class="mt-log-time">{{ formatShortTime(item.time) }}</span>
                        <span class="mt-badge" :class="`mt-badge--${item.status === 'ok' ? 'ok' : 'fail'}`">
                            {{ item.status === 'ok' ? 'OK' : 'FAIL' }}
                        </span>
                        <span class="mt-log-metrics">
                            {{ item.latency_ms != null ? `${item.latency_ms} мс` : '—' }}
                            &bull;
                            {{ item.requests_per_minute != null ? `${item.requests_per_minute} RPS` : '—' }}
                            &bull;
                            {{ item.error_rate != null ? `${item.error_rate}% err` : '—' }}
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <TemplateItemsDemo class="mb-4" />

        <!-- Integration hint -->
        <div class="mt-integration-hint">
            <Info :size="14" class="flex-shrink-0" />
            <div>
                <p class="mb-1">
                    Все метрики на этой странице — демонстрационные заглушки. Для подключения реальных данных:
                </p>
                <ul class="mt-1 mb-0 ps-3 small">
                    <li>
                        Замените логику в <code>_demo_metrics()</code> в <code>api/views.py</code> на запросы
                        к вашей системе мониторинга (Prometheus, внутренний API и т.п.).
                    </li>
                    <li>
                        Добавьте новые поля в объект, который возвращает метод <code>health</code>, и сохраните их в
                        <code>useModuleTemplateStatus</code> (история <code>history</code>).
                    </li>
                    <li>
                        Отобразите метрики на <code>StatusPage.vue</code> в виде карточек, графиков или в журнале
                        измерений. Подробный пример см. в <code>HOWTO.md</code>.
                    </li>
                </ul>
            </div>
        </div>

        <div v-if="loading" class="mt-loading-overlay">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import {
    Activity, RefreshCw, CheckCircle, XCircle, Database,
    Clock, Server, Zap, AlertTriangle, TrendingUp,
    BarChart2, List, Info,
} from 'lucide-vue-next'

import { useModuleTemplateStatus, ALERT_THRESHOLDS, getAlertLevel } from '../js/useModuleTemplate'
import TemplateItemsDemo from './TemplateItemsDemo.vue'

const HISTORY_LIMIT = 30

const {
    loading, statusData, lastUpdated, history,
    autoRefreshEnabled, autoRefreshSeconds,
    latencyLevel, rpsLevel, errorRateLevel,
    metricAggregates, refreshStatus,
    formatTime, formatShortTime, formatUptime,
    setupAutoRefresh,
} = useModuleTemplateStatus()

const latencyChart = computed(() => {
    const pts = [...history.value].reverse()
    if (pts.length < 2) return { path: '', area: '', dots: [] }
    const vals = pts.map(p => p.latency_ms ?? 0)
    const minV = Math.min(...vals)
    const range = (Math.max(...vals) - minV) || 1
    const W = 300, H = 60, pad = 5
    const coords = pts.map((p, i) => ({
        x: (i / (pts.length - 1)) * W,
        y: pad + (1 - ((p.latency_ms ?? 0) - minV) / range) * (H - pad * 2),
    }))
    const path = coords.map((c, i) => `${i === 0 ? 'M' : 'L'} ${c.x.toFixed(1)} ${c.y.toFixed(1)}`).join(' ')
    const last = coords[coords.length - 1]
    const area = `${path} L ${last.x.toFixed(1)} ${H} L 0 ${H} Z`
    return { path, area, dots: coords }
})

const rpsBars = computed(() => {
    const pts = [...history.value].reverse()
    if (!pts.length) return []
    const vals = pts.map(p => p.requests_per_minute ?? 0)
    const max = Math.max(...vals) || 1
    return vals.map(v => ({
        height: Math.max(4, (v / max) * 100),
        level: getAlertLevel(v, ALERT_THRESHOLDS.rps),
        rps: v,
    }))
})
</script>

<style lang="scss" scoped>
@import '../scss/status-page.scss';
</style>
