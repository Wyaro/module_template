# HOWTO: учебные сценарии для module_template

Этот файл дополняет `README.md` короткими практическими сценариями.

`module_template` — **живой шаблон**: любой новый паттерн платформы для модулей
сначала демонстрируется здесь (реестр `client/js/core_patterns.json`, страница «Паттерны ядра»).
Правило: `.cursor/rules/module-template-living.mdc`. Проверка: `ergoms module_template:patterns-check`.

---

## 0. Добавить демо нового паттерна ядра

1. Реализуйте демо на `PatternsPage.vue`, Status CRUD или Main (исполняемый UI/API, не только текст).
2. Добавьте запись в [`client/js/core_patterns.json`](client/js/core_patterns.json) со `status: "demoed"`, `demoFile`, `demoRoute`, `rule`.
3. Ключи подписей — в `client/js/locales/{ru,en,fr}.js` → `module_template.patterns.*`.
4. Запустите `ergoms module_template:patterns-check` (ожидается exit 0).

---

## 1. Заменить rule-based модель на свою ML-модель

1. Откройте [`api/ml_service.py`](api/ml_service.py).
2. Сохраните сигнатуру `predict(payload) -> dict` и ключи ответа.
3. Замените `_classify(...)` на вызов своей модели.
4. Обновите `get_model_meta()`.

Клиент (`MainPage.vue` + `useModuleTemplateML.js`) подхватит ответ при той же структуре.
Форма ввода — `FormCard` / `FormField` / `SelectBox` (примеры текста), не chip-кнопки.

---

## 2. Добавить метрику в health-check и StatusPage

1. В [`api/views.py`](api/views.py) расширьте `_demo_metrics()`.
2. В [`client/js/useModuleTemplate.js`](client/js/useModuleTemplate.js) — поля в `statusData` / `history`.
3. На [`StatusPage.vue`](client/components/StatusPage.vue) — карточка/график; уровни через `ALERT_THRESHOLDS`.
4. Подписи — в `locales.js` (ru / en / fr).

Перезагружаемый контент — в `LoadingContentArea`; toolbar снаружи.

---

## 3. Добавить новую страницу на клиенте

1. Компонент в `client/components/`, строки через `t('module_template.*')`.
2. Ключи в `locales.js` (все три языка).
3. Дочерний маршрут в `routes.js` — **строка** `@/modules/module_template/...`, `meta.titleKey`.
4. Пункт меню — миграция API (`MenuMigrationHelper`).

Для списков с фильтрами опирайтесь на блок [`TemplateItemsDemo.vue`](client/components/TemplateItemsDemo.vue) на StatusPage:

- `SearchInput` + `SelectBox` + `DataTable` внутри `LoadingContentArea`;
- состояние списка — `useRouteQueryState` (`page` / `q` / `active` в URL);
- create/edit — `ModalCenter` + `FormCard`/`FormField` (`defineAsyncComponent` + `v-if`);
- действия строки — `DropDown` (`compact`);
- delete — `confirmDelete`;
- строки UI — `useAppI18n()`;
- ключи API — `public_id`;
- icon-only кнопки — `aria-label`.

`client/js/locales.js` (~650 строк) близок к лимиту 700: при добавлении крупных блоков UI разнесите каталоги на `client/js/locales/{ru,en,fr}.js` и оставьте facade в `locales.js`.

---

## 4. Права и аудит

1. Ключ права — `api/permissions.py` / `permission_catalog.py`.
2. ViewSet — `BaseModelViewSet` / `BaseViewSet`, `permission_classes = [IsAuthenticated, CanViewModuleTemplate, ...]`.
3. CRUD с журналом — `AuditedModelMixin` + `AUDIT_ACTION_DEFINITIONS_GROUP`.
4. UX-guard — `permission-rules.js` с `titleKey` / `messageKey`.

В шаблоне одно право `module_template_view` закрывает весь CRUD — в боевом модуле разделите права.

---

## 5. Platform-контракты ModuleBridge

Полный каталог — [`.cursor/rules/module-contracts.mdc`](../../.cursor/rules/module-contracts.mdc).

| Контракт | Файл |
|----------|------|
| `audit.action_definitions`, `core.user_delete`, `media.upload_quota_policies` | [`api/integrations.py`](api/integrations.py) |
| `layout.plugin_registry` | [`client/js/integrations.js`](client/js/integrations.js) |
| stub session-scope (закомментирован) | те же integrations |
| `routeGuard` (passthrough) | [`client/js/routeGuard.js`](client/js/routeGuard.js) |
| Sidebar | миграции меню |

Session-scoped UI регистрирует владелец scope `<host_module>` (`SESSION_CLAIMS_GROUP` и клиентские группы). Эталон guard: `modules/<host_module>/client/js/*Guard.js`.

Межмодульные группы **не** кладите в каталог ядра. Platform-константы импортируйте из каталога ядра.

Квота загрузок: `provide_many(MEDIA_UPLOAD_QUOTA_POLICIES_GROUP, …)` в [`api/integrations.py`](api/integrations.py), частота — `MODULE_TEMPLATE_UPLOAD_RATE` в [`.env.example`](.env.example). Следующий модуль копирует этот шаблон.

---

## 6. Celery

Эталон: [`api/tasks.py`](api/tasks.py), [`api/celery_config.py`](api/celery_config.py).

```bash
ergoms start-worker
```

---

## 7. Правила Cursor модуля

Доменные инструкции агента:

- `.cursor/rules/*.mdc` — с `globs: modules/module_template/**`
- `AGENTS.md` — короткий fallback без расширения (обязателен в каждом модуле)
- `README.md` — обзор для человека (обязателен в каждом модуле)

При копировании шаблона переименуйте оба файла под новый модуль: заголовок, зависимости, команды `ergoms <name>:…`.

После добавления или правки `.mdc`: расширение **ERGO MS Module Cursor Rules** синхронизирует staging само (или команда **ERGO MS: Sync Module Cursor Rules**). Установка: `ergoms install-extensions`.

---

## 8. Команды

```bash
ergoms module_template:patterns-check
ergoms module_template:migrate
ergoms dev
ergoms start-client
ergoms help module module_template
```

---

## 9. Footprint задач для балансировщика Celery

Эталон: [`task_footprint.yaml`](task_footprint.yaml). Ядро читает файл через hook discovery (`ergoms celery-balance`), без импорта `api/` модуля.

1. Скопируйте YAML в новый модуль и замените очередь/`pattern` на свои.
2. Для тяжёлых задач укажите `class: heavy`, `ram_mb`, `max_parallel`; для GPU — `gpu_required`, `vram_mb` и при необходимости `cpu_fallback: false` (без устройства очередь ставится на паузу).
3. Проверка отчёта: `ergoms celery-balance --dry-run`.

---

## 10. Вынос модуля в отдельный сервис

Живой эталон файлов уровня 1–2. Подробности — [`.docs/modularization.md`](../../.docs/modularization.md).

1. `api/bridge_manifest.yaml` — владелец ops/groups для HTTP-моста.
2. `api/schema.yaml` — схема `m_<name>`, `isolated: true` (нет FK на пользователя ядра).
3. `host_lifecycle.yaml` / `process_roles.yaml` — OS-службы через `ergoms install-module-service`.
4. Проверка инфраструктуры: `MODULE_RUNTIME=microservice`, `MICROSERVICE_MODULES=module_template`, `ergoms start-module --module=module_template`.
5. Очередь Celery уже `module_template`; worker: `ergoms start-worker --module=module_template`.
6. Разработка по умолчанию остаётся монолитом (`MODULE_RUNTIME=monolith`).

