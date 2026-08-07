<script setup>
/**
 * Живой каталог паттернов ядра: реестр из core_patterns.json + песочница UI.
 * Оболочка страницы — admin-page / page-header / content-card (стандарт ядра).
 */
import { computed, ref } from 'vue'
import { CheckCircle2, CircleDashed } from 'lucide-vue-next'
import DecimalInput from '@/components/DecimalInput.vue'
import FilterMenu from '@/components/FilterMenu.vue'
import FormCard from '@/components/FormCard.vue'
import FormField from '@/components/FormField.vue'
import { useAppI18n } from '@/i18n/useAppI18n.js'
import { confirmAction } from '@/js/utils/confirm.js'
import { useToast } from '@/js/utils/toast.js'

import catalog from '../js/core_patterns.json'

const { t } = useAppI18n()
const toast = useToast()

const patterns = computed(() => catalog.patterns || [])

const demoedCount = computed(
  () => patterns.value.filter((item) => item.status === 'demoed').length,
)

const filters = ref({ category: '', priority: '' })
const decimalValue = ref('12,5')
const formName = ref('')
const formNote = ref('')
const formActive = ref(true)

const filterFields = computed(() => [
  { type: 'heading', label: t('module_template.patterns.filterCategory') },
  {
    type: 'select',
    key: 'category',
    label: t('module_template.patterns.filterCategory'),
    options: [
      { id: 'bug', name: t('module_template.ml.categories.error') },
      { id: 'request', name: t('module_template.ml.categories.request') },
      { id: 'report', name: t('module_template.ml.categories.report') },
    ],
    valueKey: 'id',
    labelKey: 'name',
    includeAllOption: true,
    allLabel: t('module_template.patterns.filterAll'),
  },
  { type: 'heading', label: t('module_template.patterns.filterPriority') },
  {
    type: 'select',
    key: 'priority',
    label: t('module_template.patterns.filterPriority'),
    options: [
      { id: 'high', name: t('module_template.ml.priorities.high') },
      { id: 'medium', name: t('module_template.ml.priorities.medium') },
      { id: 'low', name: t('module_template.ml.priorities.low') },
    ],
    valueKey: 'id',
    labelKey: 'name',
    includeAllOption: true,
    allLabel: t('module_template.patterns.filterAll'),
  },
])

const onFiltersApply = () => {
  toast.info(t('module_template.patterns.applyFilters'))
}

const showToastDemo = () => {
  toast.success(t('module_template.patterns.toastDemoText'))
}

const showConfirmDemo = async () => {
  const ok = await confirmAction({
    title: t('module_template.patterns.confirmTitle'),
    message: t('module_template.patterns.confirmMessage'),
    variant: 'primary',
  })
  if (ok) {
    toast.success(t('module_template.patterns.toastDemoText'))
  }
}

const statusLabel = (status) =>
  status === 'demoed'
    ? t('module_template.patterns.statusDemoed')
    : t('module_template.patterns.statusPlanned')
</script>

<template>
  <div class="admin-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">{{ t('module_template.patterns.title') }}</h1>
        <p class="page-subtitle">{{ t('module_template.patterns.subtitle') }}</p>
        <p class="page-header__meta">
          {{ demoedCount }} / {{ patterns.length }} · {{ t('module_template.patterns.checkHint') }}
        </p>
      </div>
    </div>

    <div class="content-card">
      <h2 class="section-heading">{{ t('module_template.patterns.catalogHeading') }}</h2>
      <ul class="mt-patterns-catalog">
        <li
          v-for="item in patterns"
          :key="item.id"
          class="mt-patterns-catalog__item"
        >
          <div class="mt-patterns-catalog__main">
            <span
              class="mt-patterns-catalog__status"
              :class="item.status === 'demoed'
                ? 'mt-patterns-catalog__status--ok'
                : 'mt-patterns-catalog__status--planned'"
            >
              <CheckCircle2 v-if="item.status === 'demoed'" :size="14" />
              <CircleDashed v-else :size="14" />
              {{ statusLabel(item.status) }}
            </span>
            <h3 class="mt-patterns-catalog__title">{{ t(item.titleKey) }}</h3>
            <p class="mt-patterns-catalog__desc">{{ t(item.descKey) }}</p>
            <div class="mt-patterns-catalog__meta">
              <span>{{ t('module_template.patterns.ruleLabel') }}: {{ item.rule }}</span>
              <span>{{ t('module_template.patterns.fileLabel') }}: {{ item.demoFile }}</span>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <div class="content-card">
      <h2 class="section-heading">{{ t('module_template.patterns.playgroundHeading') }}</h2>
      <p class="mt-patterns-playground__hint">{{ t('module_template.patterns.playgroundHint') }}</p>

      <div class="table-header">
        <div class="actions-wrapper">
          <FilterMenu
            v-model="filters"
            :fields="filterFields"
            :trigger-label="t('module_template.patterns.filterMenuLabel')"
            apply-on-change
            @apply="onFiltersApply"
          />
          <button
            type="button"
            class="ui-btn ui-btn--secondary"
            @click="showToastDemo"
          >
            {{ t('module_template.patterns.toastDemo') }}
          </button>
          <button
            type="button"
            class="ui-btn ui-btn--secondary"
            @click="showConfirmDemo"
          >
            {{ t('module_template.patterns.confirmDemo') }}
          </button>
        </div>
      </div>

      <FormCard>
        <FormField
          :label="t('module_template.patterns.formName')"
          label-for="mt-pattern-name"
        >
          <input
            id="mt-pattern-name"
            v-model="formName"
            type="text"
            class="form-control form-control-sm"
          />
        </FormField>
        <FormField
          :label="t('module_template.patterns.formScore')"
          label-for="mt-pattern-score"
          :hint="t('module_template.patterns.decimalHint')"
        >
          <DecimalInput
            id="mt-pattern-score"
            v-model="decimalValue"
            input-class="form-control-sm"
            :aria-label="t('module_template.patterns.decimalLabel')"
            :show-steppers="true"
            :step="0.5"
          />
        </FormField>
        <FormField
          :label="t('module_template.patterns.formOptional')"
          label-for="mt-pattern-note"
          optional
        >
          <input
            id="mt-pattern-note"
            v-model="formNote"
            type="text"
            class="form-control form-control-sm"
          />
        </FormField>
        <FormField
          :label="t('module_template.patterns.formActive')"
          label-for="mt-pattern-active"
          align="center"
          last
        >
          <input
            id="mt-pattern-active"
            v-model="formActive"
            class="form-check-input"
            type="checkbox"
          />
        </FormField>
      </FormCard>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '../scss/page-shell.scss';

.mt-patterns-catalog {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.mt-patterns-catalog__item {
  padding: 0.9rem 1rem;
  border: 1px solid var(--ui-border);
  border-radius: var(--ui-radius, 0.5rem);
  background: var(--ui-surface-2);
}

.mt-patterns-catalog__title {
  margin: 0.35rem 0 0.2rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--ui-text);
}

.mt-patterns-catalog__desc {
  margin: 0;
  font-size: 0.82rem;
  color: var(--ui-text-muted);
  max-width: 40rem;
}

.mt-patterns-catalog__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.45rem;
  font-size: 0.72rem;
  color: var(--ui-text-muted);
  font-family: var(--font-family-mono);
}

.mt-patterns-catalog__status {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: var(--ui-pill);

  &--ok {
    background: var(--ui-accent-soft);
    color: var(--ui-accent);
  }

  &--planned {
    background: var(--ui-surface);
    color: var(--ui-text-muted);
    border: 1px solid var(--ui-border);
  }
}

.mt-patterns-playground__hint {
  margin: 0;
  font-size: 0.875rem;
  color: var(--ui-text-muted);
}
</style>
