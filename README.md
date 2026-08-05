# Module Template (module_template)

**Живой шаблон** ERGO MS: отправная точка для новых модулей и обязательное место демо
новых паттернов платформы для модулей (см. `.cursor/rules/module-template-living.mdc`).

В одном месте собраны:

- health-check и мониторинг сервиса,
- rule-based «ML-модель»,
- типовой CRUD API и Vue-клиент на компонентах ядра,
- каталог паттернов (`core_patterns.json` + страница «Паттерны ядра»),
- права модуля, аудит CRUD и i18n через hook `locales.js`.

---

## 1. Структура модуля

```text
modules/module_template/
├── integrations.yaml          # requires / extends (зависимости модулей)
├── api/
│   ├── apps.py                # AppConfig (ready → integrations)
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
│   │   ├── routes.js          # Main + Status + Patterns
│   │   ├── endpoints.js
│   │   ├── locales.js         # facade → locales/{ru,en,fr}.js
│   │   ├── core_patterns.json # реестр эталонов для patterns-check
│   │   ├── permission-rules.js
│   │   ├── integrations.js
│   │   ├── routeGuard.js
│   │   ├── useModuleTemplate.js
│   │   └── useModuleTemplateML.js
│   ├── components/
│   │   ├── MainPage.vue
│   │   ├── StatusPage.vue
│   │   ├── PatternsPage.vue       # каталог + песочница паттернов ядра
│   │   ├── TemplateItemsDemo.vue  # CRUD-блок на Status (компоненты ядра)
│   │   └── TemplateItemModal.vue  # ModalCenter + FormCard/FormField
│   ├── ParentLayout.vue
│   ├── package.json
│   ├── scss/
│   └── assets/
├── scripts/
│   └── patterns_check.py      # ergoms module_template:patterns-check
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
ergoms module_template:patterns-check
ergoms module_template:migrate
ergoms dev
ergoms start-client
```

После запуска:

1. Главная (`ModuleTemplateMain`) — ML-демо.
2. Статус (`ModuleTemplateStatus`) — health, метрики и блок TemplateItem (CRUD на компонентах ядра).
3. Паттерны (`ModuleTemplatePatterns`) — живой каталог эталонов и песочница UI.

Нужно право `module_template_view` (или глобальный администратор).

---

## 3. UI модуля (компоненты ядра)

Страницы модуля используют те же компоненты, что и ядро:

| Место | Компоненты |
|-------|------------|
| Status (метрики) | `LoadingContentArea` |
| Status (список TemplateItem) | `SearchInput`, `SelectBox`, `DataTable`, `DropDown`, `LoadingContentArea`, `ModalCenter` + `FormCard`/`FormField`, `confirmDelete` |
| Patterns | `FilterMenu`, `DecimalInput`, `FormCard`/`FormField`, toast, confirm, реестр `core_patterns.json` |
| Main (ML) | `ContentImage`, toast, `logError`, `useAppI18n` |
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
