# Module Template (module_template)

Учебный модуль для системы ERGO MS. Показывает, как в одном месте собрать:

- health-check и мониторинг сервиса,
- простую rule-based «ML-модель»,
- типовой CRUD API и Vue-клиент на компонентах ядра,
- права модуля, аудит CRUD и i18n через hook `locales.js`.

Модуль задуман как отправная точка для студенческих и исследовательских модулей СКБ.

---

## 1. Структура модуля

```text
modules/module_template/
├── api/
│   ├── apps.py                # AppConfig (ready → integrations; пример module_requires)
│   ├── config.py
│   ├── models.py              # TemplateItem (public_id)
│   ├── serializers.py
│   ├── views.py               # TemplateItemViewSet + HealthViewSet + ML
│   ├── permissions.py
│   ├── permission_catalog.py
│   ├── integrations.py        # ModuleBridge: audit, core.user_delete; stub session-scope
│   ├── tasks.py               # эталон Celery @shared_task
│   ├── celery_config.py       # маршруты очереди module_template
│   ├── ml_service.py
│   ├── urls.py
│   ├── locale/                # gettext ru/en/fr
│   └── migrations/
├── client/
│   ├── js/
│   │   ├── routes.js          # Main + Status
│   │   ├── endpoints.js
│   │   ├── locales.js         # ru / en / fr
│   │   ├── permission-rules.js
│   │   ├── integrations.js
│   │   ├── routeGuard.js
│   │   ├── useModuleTemplate.js
│   │   └── useModuleTemplateML.js
│   ├── components/
│   │   ├── MainPage.vue
│   │   ├── StatusPage.vue
│   │   ├── TemplateItemsDemo.vue  # CRUD-блок на Status (компоненты ядра)
│   │   └── TemplateItemModal.vue  # ModalCenter create/edit
│   ├── ParentLayout.vue
│   ├── package.json
│   ├── scss/
│   └── assets/
├── mcp/                       # эталон manifest (без server.py — не регистрируется)
├── .cursor/rules/             # правила Cursor модуля (*.mdc)
├── AGENTS.md                  # fallback для агента без расширения
├── ergoms.conf
├── ergoms.help.yaml
├── vscode.tasks.yaml          # задачи Run Task (ergo-module)
├── HOWTO.md
└── README.md
```

Правила агента Cursor для этого модуля — в `.cursor/rules/` и кратко в `AGENTS.md`. Подхват `.mdc` в Cursor: расширение **ERGO MS Module Cursor Rules** (`ergoms install-extensions`).

---

## 2. Как запустить

```bash
ergoms module_template:migrate
ergoms dev
ergoms start-client
```

После запуска:

1. Главная (`ModuleTemplateMain`) — ML-демо.
2. Статус (`ModuleTemplateStatus`) — health, метрики (`LoadingContentArea`) и блок TemplateItem (DataTable / ModalCenter / confirm).

Нужно право `module_template_view` (или глобальный администратор).

---

## 3. UI модуля (компоненты ядра)

Страницы модуля используют те же компоненты, что и ядро:

| Место | Компоненты |
|-------|------------|
| Status (метрики) | `LoadingContentArea` |
| Status (список TemplateItem) | `SearchInput`, `SelectBox`, `DataTable`, `LoadingContentArea`, `ModalCenter`, `confirmDelete` |
| Main (ML) | `ContentImage`, toast, `logError`, строки из `locales.js` |
| Lookup API | `public_id`, не pk БД |

---

## 4. API

- `GET /api/module_template/health/`
- `GET /api/module_template/model-meta/`, `POST …/predict/`
- `/api/module_template/items/` — CRUD по `public_id`; query: `search`, `active`, `page`, `page_size`

---

## 5. i18n

Клиент: `locales.js` — **ru / en / fr**. Сервер: `_()` / gettext в `api/locale/`.

---

## 6. Стили и тема

`--ui-*` (приоритет над `--bs-*`). `theme-defaults.js` не нужен, пока хватает палитры сайта.

По необходимости: `clientEnv.js`, `process_roles.yaml` / `host_lifecycle.yaml`, `vscode.tasks.yaml`, `theme-defaults.js`.

---

## 7. Rename-чеклист при копировании

1. Папка `modules/<name>/`.
2. `AppConfig.name` / `label`.
3. Permission keys, audit prefixes, bridge op names.
4. Route names, locales namespace.
5. `ergoms.conf` / MCP name.
6. `vscode.tasks.yaml` — label/command под новый модуль (если нужны задачи в Run Task).
7. Меню — миграция `MenuMigrationHelper(apps, 'modules/<name>')`.

---

## 8. Импорты

**API:** относительные внутри модуля; из ядра — `from src.core...`.  
**Клиент:** `@/...` из ядра; относительные внутри модуля.  
Между модулями — только ModuleBridge.

---

## 9. Расширение

См. [`HOWTO.md`](HOWTO.md).
