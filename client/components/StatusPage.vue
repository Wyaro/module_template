<template>
    <div class="admin-page mt-status-page">
        <div class="page-header">
            <div>
                <h1 class="page-title">{{ t('module_template.status.pageTitle') }}</h1>
                <p class="page-subtitle">{{ t('module_template.status.pageSubtitle') }}</p>
                <p class="page-header__meta">
                    {{ t('module_template.status.lastUpdated') }}
                    <strong>{{ formatTime(lastUpdated || statusData.time) }}</strong>
                </p>
            </div>
            <div
                class="page-header__actions mt-controls"
                role="group"
                :aria-label="t('module_template.status.monitoringBadge')"
            >
                <span class="mt-monitoring-badge">{{ t('module_template.status.monitoringBadge') }}</span>
                <div class="form-check form-switch mt-auto-refresh mb-0">
                    <input
                        id="mt-auto-refresh"
                        v-model="autoRefreshEnabled"
                        class="form-check-input"
                        type="checkbox"
                        role="switch"
                        @change="setupAutoRefresh"
                    />
                    <label class="mt-auto-refresh__label" for="mt-auto-refresh">
                        {{ t('module_template.status.autoRefresh', { seconds: autoRefreshSeconds }) }}
                    </label>
                </div>
                <button
                    type="button"
                    class="ui-btn ui-btn--secondary mt-controls__refresh"
                    :disabled="isBusy"
                    :aria-busy="isBusy"
                    @click="refreshStatus"
                >
                    <RefreshCw :size="16" :class="{ spin: isBusy }" />
                    <span>{{ t('module_template.status.refresh') }}</span>
                </button>
            </div>
        </div>

        <LoadingContentArea
            :loading="isBusy"
            min-height="16rem"
            :loading-text="t('module_template.loading')"
        >
            <div class="content-card">
                <div class="row g-3">
                    <div class="col-sm-6 col-xl-3">
                        <div class="mt-card" :class="`mt-card--${statusData.status === 'ok' ? 'ok' : 'fail'}`">
                            <div class="mt-card-icon">
                                <CheckCircle v-if="statusData.status === 'ok'" :size="20" />
                                <XCircle v-else :size="20" />
                            </div>
                            <div class="mt-card-body">
                                <span class="mt-card-label">{{ t('module_template.status.service') }}</span>
                                <span class="mt-card-value">
                                    {{ statusData.status === 'ok' ? t('module_template.status.serviceOk') : t('module_template.status.serviceFail') }}
                                </span>
                            </div>
                            <span class="mt-badge" :class="`mt-badge--${statusData.status === 'ok' ? 'ok' : 'fail'}`">
                                {{ statusData.status === 'ok' ? badgeOk : badgeFail }}
                            </span>
                        </div>
                    </div>

                    <div class="col-sm-6 col-xl-3">
                        <div class="mt-card" :class="`mt-card--${statusData.db === 'ok' ? 'ok' : 'fail'}`">
                            <div class="mt-card-icon">
                                <Database :size="20" />
                            </div>
                            <div class="mt-card-body">
                                <span class="mt-card-label">{{ t('module_template.status.database') }}</span>
                                <span class="mt-card-value">
                                    {{ statusData.db === 'ok' ? t('module_template.status.dbOk') : t('module_template.status.dbFail') }}
                                </span>
                            </div>
                            <span class="mt-badge" :class="`mt-badge--${statusData.db === 'ok' ? 'ok' : 'fail'}`">
                                {{ statusData.db === 'ok' ? badgeOk : badgeFail }}
                            </span>
                        </div>
                    </div>

                    <div class="col-sm-6 col-xl-3">
                        <div class="mt-card mt-card--neutral">
                            <div class="mt-card-icon">
                                <Clock :size="20" />
                            </div>
                            <div class="mt-card-body">
                                <span class="mt-card-label">{{ t('module_template.status.uptime') }}</span>
                                <span class="mt-card-value">{{ formatUptime(statusData.uptime_seconds) }}</span>
                            </div>
                            <span class="mt-badge mt-badge--neutral">{{ statusData.environment }}</span>
                        </div>
                    </div>

                    <div class="col-sm-6 col-xl-3">
                        <div class="mt-card mt-card--neutral">
                            <div class="mt-card-icon">
                                <Server :size="20" />
                            </div>
                            <div class="mt-card-body">
                                <span class="mt-card-label">{{ t('module_template.status.nodeVersion') }}</span>
                                <span class="mt-card-value">{{ statusData.node_name }}</span>
                            </div>
                            <span class="mt-badge mt-badge--neutral">v{{ statusData.app_version }}</span>
                        </div>
                    </div>
                </div>

                <div class="row g-3">
                    <div class="col-md-4">
                        <div class="mt-metric-card" :class="`mt-metric-card--${latencyLevel}`">
                            <div class="mt-metric-header">
                                <Activity :size="16" />
                                <span>{{ t('module_template.status.latency') }}</span>
                                <span class="mt-badge ms-auto" :class="`mt-badge--${latencyLevel}`">
                                    {{ levelLabel(latencyLevel) }}
                                </span>
                            </div>
                            <div class="mt-metric-value">
                                {{ statusData.latency_ms != null ? t('module_template.status.ms', { value: statusData.latency_ms }) : '—' }}
                            </div>
                            <div class="mt-metric-bar">
                                <div
                                    class="mt-metric-bar-fill"
                                    :class="`mt-metric-bar-fill--${latencyLevel}`"
                                    :style="{ width: `${Math.min(100, ((statusData.latency_ms ?? 0) / 200) * 100)}%` }"
                                />
                            </div>
                            <div v-if="metricAggregates.latencyAvg != null" class="mt-metric-aggregates">
                                <span>{{ t('module_template.status.latencyAvg', { value: metricAggregates.latencyAvg }) }}</span>
                                <span>{{ t('module_template.status.latencyMin', { value: metricAggregates.latencyMin }) }}</span>
                                <span>{{ t('module_template.status.latencyMax', { value: metricAggregates.latencyMax }) }}</span>
                            </div>
                            <p class="mt-metric-hint">{{ t('module_template.status.latencyHint') }}</p>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="mt-metric-card" :class="`mt-metric-card--${rpsLevel}`">
                            <div class="mt-metric-header">
                                <Zap :size="16" />
                                <span>{{ t('module_template.status.rps') }}</span>
                                <span class="mt-badge ms-auto" :class="`mt-badge--${rpsLevel}`">
                                    {{ levelLabel(rpsLevel) }}
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
                                />
                            </div>
                            <div v-if="metricAggregates.rpsAvg != null" class="mt-metric-aggregates">
                                <span>{{ t('module_template.status.rpsAvg', { value: metricAggregates.rpsAvg }) }}</span>
                            </div>
                            <p class="mt-metric-hint">{{ t('module_template.status.rpsHint') }}</p>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="mt-metric-card" :class="`mt-metric-card--${errorRateLevel}`">
                            <div class="mt-metric-header">
                                <AlertTriangle :size="16" />
                                <span>{{ t('module_template.status.errorRate') }}</span>
                                <span class="mt-badge ms-auto" :class="`mt-badge--${errorRateLevel}`">
                                    {{ levelLabel(errorRateLevel) }}
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
                                />
                            </div>
                            <div v-if="metricAggregates.errorRateAvg != null" class="mt-metric-aggregates">
                                <span>{{ t('module_template.status.errorRateAvg', { value: metricAggregates.errorRateAvg }) }}</span>
                            </div>
                            <p class="mt-metric-hint">{{ t('module_template.status.errorRateHint') }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row g-3">
                <div class="col-lg-8">
                    <div class="content-card mt-chart-card h-100">
                        <header class="mt-chart-head">
                            <TrendingUp :size="16" class="mt-chart-head__icon" aria-hidden="true" />
                            <div class="mt-chart-head__body">
                                <h2 class="mt-chart-head__title">
                                    {{ t('module_template.status.chartLatencyTitle') }}
                                    <span class="mt-chart-head__demo">{{ t('module_template.status.demo') }}</span>
                                </h2>
                                <p class="mt-chart-head__subtitle">
                                    {{ t('module_template.status.chartLatencySubtitle') }}
                                </p>
                            </div>
                        </header>

                        <div v-if="latencyChart.path" class="mt-line-chart">
                            <svg
                                viewBox="0 0 300 64"
                                preserveAspectRatio="none"
                                width="100%"
                                height="80"
                            >
                                <defs>
                                    <linearGradient id="mt-latency-grad" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="0%" style="stop-color: var(--ui-accent); stop-opacity: 0.2" />
                                        <stop offset="100%" style="stop-color: var(--ui-accent); stop-opacity: 0" />
                                    </linearGradient>
                                </defs>
                                <path :d="latencyChart.area" fill="url(#mt-latency-grad)" />
                                <path
                                    :d="latencyChart.path"
                                    fill="none"
                                    :style="{ stroke: 'var(--ui-accent)', strokeWidth: '1.5', strokeLinejoin: 'round' }"
                                />
                                <circle
                                    v-if="latencyChart.dots.length"
                                    :cx="latencyChart.dots[latencyChart.dots.length - 1].x"
                                    :cy="latencyChart.dots[latencyChart.dots.length - 1].y"
                                    r="3"
                                    :style="{ fill: 'var(--ui-accent)' }"
                                />
                            </svg>
                            <div class="mt-chart-labels">
                                <span>{{ formatShortTime(history[history.length - 1]?.time) }}</span>
                                <span>{{ formatShortTime(history[0]?.time) }}</span>
                            </div>
                        </div>
                        <div v-else class="mt-chart-empty">
                            {{ t('module_template.status.chartEmpty') }}
                        </div>
                    </div>
                </div>

                <div class="col-lg-4">
                    <div class="content-card mt-chart-card h-100">
                        <header class="mt-chart-head">
                            <BarChart2 :size="16" class="mt-chart-head__icon" aria-hidden="true" />
                            <div class="mt-chart-head__body">
                                <h2 class="mt-chart-head__title">
                                    {{ t('module_template.status.chartRpsTitle') }}
                                    <span class="mt-chart-head__demo">{{ t('module_template.status.demo') }}</span>
                                </h2>
                                <p class="mt-chart-head__subtitle">
                                    {{ t('module_template.status.chartRpsSubtitle') }}
                                </p>
                            </div>
                        </header>

                        <div v-if="rpsBars.length" class="mt-bar-chart">
                            <div
                                v-for="(bar, i) in rpsBars"
                                :key="i"
                                class="mt-bar"
                                :class="`mt-bar--${bar.level}`"
                                :style="{ height: `${bar.height}%` }"
                                :title="`${bar.rps} RPS`"
                            />
                        </div>
                        <div v-else class="mt-chart-empty">
                            {{ t('module_template.status.chartEmpty') }}
                        </div>
                    </div>
                </div>
            </div>

            <div class="content-card">
                <div class="table-header">
                    <h2 class="section-heading">
                        <List :size="16" class="section-heading__icon" />
                        {{ t('module_template.status.historyTitle') }}
                    </h2>
                    <span class="text-muted small">
                        {{ t('module_template.status.historyCount', { count: history.length, limit: HISTORY_LIMIT }) }}
                    </span>
                </div>
                <div v-if="!history.length" class="text-muted small py-2">
                    {{ t('module_template.status.historyEmpty') }}
                </div>
                <div v-else class="mt-history-log">
                    <div
                        v-for="(item, i) in history"
                        :key="`${item.time}-${i}`"
                        class="mt-log-row"
                        :class="{
                            'mt-log-row--ok': item.status === 'ok' && item.db === 'ok',
                            'mt-log-row--warn': item.status === 'ok' && item.db !== 'ok',
                            'mt-log-row--fail': item.status !== 'ok',
                        }"
                    >
                        <div class="mt-log-dot" />
                        <span class="mt-log-time">{{ formatShortTime(item.time) }}</span>
                        <span class="mt-badge" :class="`mt-badge--${item.status === 'ok' ? 'ok' : 'fail'}`">
                            {{ item.status === 'ok' ? badgeOk : badgeFail }}
                        </span>
                        <span class="mt-log-metrics">
                            {{ item.latency_ms != null ? t('module_template.status.ms', { value: item.latency_ms }) : '—' }}
                            &bull;
                            {{ item.requests_per_minute != null ? `${item.requests_per_minute} RPS` : '—' }}
                            &bull;
                            {{ item.error_rate != null ? `${item.error_rate}% err` : '—' }}
                        </span>
                    </div>
                </div>
            </div>
        </LoadingContentArea>

        <TemplateItemsDemo />

        <aside class="mt-integration-hint">
            <Info :size="16" class="mt-integration-hint__icon" aria-hidden="true" />
            <div class="mt-integration-hint__body">
                <p class="mt-integration-hint__title">
                    {{ t('module_template.status.integrationTitle') }}
                </p>
                <ul class="mt-integration-hint__list">
                    <li>{{ t('module_template.status.integrationStep1') }}</li>
                    <li>{{ t('module_template.status.integrationStep2') }}</li>
                    <li>{{ t('module_template.status.integrationStep3') }}</li>
                </ul>
            </div>
        </aside>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import {
    Activity, RefreshCw, CheckCircle, XCircle, Database,
    Clock, Server, Zap, AlertTriangle, TrendingUp,
    BarChart2, List, Info,
} from 'lucide-vue-next'

import LoadingContentArea from '@/components/LoadingContentArea.vue'
import { useAppI18n } from '@/i18n/useAppI18n.js'
import { useModuleTemplateStatus, ALERT_THRESHOLDS, getAlertLevel } from '../js/useModuleTemplate'
import TemplateItemsDemo from './TemplateItemsDemo.vue'

const HISTORY_LIMIT = 30
const { t } = useAppI18n()

const {
    isBusy, statusData, lastUpdated, history,
    autoRefreshEnabled, autoRefreshSeconds,
    latencyLevel, rpsLevel, errorRateLevel,
    metricAggregates, refreshStatus,
    formatTime, formatShortTime, formatUptime,
    setupAutoRefresh,
} = useModuleTemplateStatus()

const badgeOk = computed(() => t('module_template.status.badgeOk'))
const badgeFail = computed(() => t('module_template.status.badgeFail'))

const levelLabel = (level) => t(`module_template.status.levels.${level}`)

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
@import '../scss/page-shell.scss';
@import '../scss/status-page.scss';
</style>
