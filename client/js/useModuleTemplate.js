import { ref, computed, onMounted, onUnmounted } from 'vue'
import { apiClient } from '@/js/api/manager'
import { useToast } from '@/js/utils/toast.js'

import { moduleTemplateEndpoints } from './endpoints'

const HISTORY_LIMIT = 30
const AUTO_REFRESH_SECONDS = 10

export const ALERT_THRESHOLDS = {
    latency: { warn: 80, crit: 150 },
    rps:     { warn: 50, crit: 80 },
    error:   { warn: 2,  crit: 5 },
}

export const getAlertLevel = (value, thresholds) => {
    if (value == null) return 'ok'
    if (value >= thresholds.crit) return 'crit'
    if (value >= thresholds.warn) return 'warn'
    return 'ok'
}

const avg = (arr) => arr.length ? arr.reduce((s, v) => s + v, 0) / arr.length : null

export function useModuleTemplateStatus() {
    const toast = useToast()
    const loading = ref(false)
    const statusData = ref({
        status: 'unknown',
        db: 'unknown',
        time: null,
        app_version: '-',
        latency_ms: null,
        requests_per_minute: null,
        error_rate: null,
        uptime_seconds: null,
        environment: '-',
        node_name: '-',
    })

    const lastUpdated = ref(null)
    const history = ref([])
    const autoRefreshEnabled = ref(true)
    const autoRefreshSeconds = ref(AUTO_REFRESH_SECONDS)
    let intervalId = null

    const latencyLevel  = computed(() => getAlertLevel(statusData.value.latency_ms, ALERT_THRESHOLDS.latency))
    const rpsLevel      = computed(() => getAlertLevel(statusData.value.requests_per_minute, ALERT_THRESHOLDS.rps))
    const errorRateLevel = computed(() => getAlertLevel(statusData.value.error_rate, ALERT_THRESHOLDS.error))

    const metricAggregates = computed(() => {
        const latencies = history.value.map(h => h.latency_ms).filter(v => v != null)
        const rpsValues = history.value.map(h => h.requests_per_minute).filter(v => v != null)
        const errValues = history.value.map(h => h.error_rate).filter(v => v != null)
        return {
            latencyAvg: latencies.length ? Math.round(avg(latencies) * 10) / 10 : null,
            latencyMin: latencies.length ? Math.round(Math.min(...latencies) * 10) / 10 : null,
            latencyMax: latencies.length ? Math.round(Math.max(...latencies) * 10) / 10 : null,
            rpsAvg:     rpsValues.length ? Math.round(avg(rpsValues) * 10) / 10 : null,
            errorRateAvg: errValues.length ? Math.round(avg(errValues) * 100) / 100 : null,
        }
    })

    const refreshStatus = async () => {
        loading.value = true
        try {
            const response = await apiClient.get(moduleTemplateEndpoints.moduleTemplate.health)
            if (response.success) {
                statusData.value = response.data
                lastUpdated.value = new Date().toISOString()
                history.value = [
                    {
                        time: response.data.time,
                        status: response.data.status,
                        db: response.data.db,
                        latency_ms: response.data.latency_ms,
                        requests_per_minute: response.data.requests_per_minute,
                        error_rate: response.data.error_rate,
                    },
                    ...history.value.slice(0, HISTORY_LIMIT - 1),
                ]
            } else {
                if (response.data) statusData.value = response.data
                toast.warning(response.message || 'Сервис недоступен')
                lastUpdated.value = new Date().toISOString()
            }
        } catch (error) {
            statusData.value = { ...statusData.value, status: 'fail', db: 'fail' }
            toast.error('Ошибка подключения к серверу')
            logError('Health check error:', error)
            lastUpdated.value = new Date().toISOString()
        } finally {
            loading.value = false
        }
    }

    const formatTime = (isoString) => {
        if (!isoString) return '-'
        try {
            return new Date(isoString).toLocaleString('ru-RU', {
                day: '2-digit', month: '2-digit', year: 'numeric',
                hour: '2-digit', minute: '2-digit', second: '2-digit',
            })
        } catch { return isoString }
    }

    const formatShortTime = (isoString) => {
        if (!isoString) return '-'
        try {
            return new Date(isoString).toLocaleTimeString('ru-RU', {
                hour: '2-digit', minute: '2-digit', second: '2-digit',
            })
        } catch { return isoString }
    }

    const formatUptime = (seconds) => {
        if (seconds == null) return '-'
        const d = Math.floor(seconds / 86400)
        const h = Math.floor((seconds % 86400) / 3600)
        const m = Math.floor((seconds % 3600) / 60)
        const s = seconds % 60
        if (d > 0) return `${d}д ${h}ч ${m}м`
        if (h > 0) return `${h}ч ${m}м ${s}с`
        if (m > 0) return `${m}м ${s}с`
        return `${s}с`
    }

    const setupAutoRefresh = () => {
        if (intervalId) {
            clearInterval(intervalId)
            intervalId = null
        }
        if (!autoRefreshEnabled.value) return
        intervalId = setInterval(() => {
            if (!loading.value) refreshStatus()
        }, autoRefreshSeconds.value * 1000)
    }

    onMounted(() => {
        refreshStatus()
        setupAutoRefresh()
    })

    onUnmounted(() => {
        if (intervalId) clearInterval(intervalId)
    })

    return {
        loading,
        statusData,
        lastUpdated,
        history,
        autoRefreshEnabled,
        autoRefreshSeconds,
        latencyLevel,
        rpsLevel,
        errorRateLevel,
        metricAggregates,
        refreshStatus,
        formatTime,
        formatShortTime,
        formatUptime,
        setupAutoRefresh,
    }
}
