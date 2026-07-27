# Module Template (module_template)

Учебный модуль для системы ERGO MS. Показывает, как в одном месте собрать:

- health‑check и мониторинг сервиса,
- простую rule‑based «ML‑модель»,
- типовой CRUD‑API и Vue‑клиент,
- права модуля, аудит CRUD и i18n через hook `locales.js`.

Модуль задуман как отправная точка для студенческих и исследовательских модулей СКБ.

---

## 1. Структура модуля

```text
modules/module_template/
├── api/                       # Серверная часть (Django + DRF)
│   ├── apps.py                # AppConfig модуля (ready → integrations)
│   ├── config.py              # Константы (MODULE_DATABASE_ALIAS, VERSION, USE_GPU)
│   ├── models.py              # TemplateItem (public_id)
│   ├── serializers.py         # TemplateItemSerializer
│   ├── views.py               # TemplateItemViewSet, HealthViewSet, ML endpoints
│   ├── permissions.py         # CanViewModuleTemplate (BaseModulePermission)
│   ├── permission_catalog.py  # Каталог прав для ADP
│   ├── integrations.py        # ModuleBridge: audit, core.user_delete, health stub
│   ├── ml_service.py          # Rule-based модель для текста (demo)
│   ├── urls.py                # URL-маршруты модуля
│   └── migrations/
├── client/                    # Клиентская часть (Vue)
│   ├── js/
│   │   ├── routes.js          # Маршруты Vue Router (titleKey, lazy string paths)
│   │   ├── endpoints.js       # Эндпоинты API модуля
│   │   ├── locales.js         # ru/en pack (namespace module_template)
│   │   ├── permission-rules.js
│   │   ├── integrations.js    # layout.plugin_registry
│   │   ├── routeGuard.js      # passthrough (session-scope — в ядре)
│   │   ├── useModuleTemplate.js   # Health‑check и метрики
│   │   └── useModuleTemplateML.js # Работа с ML‑эндпоинтами
│   ├── components/
│   │   ├── MainPage.vue       # Главный экран модуля СКБ
│   │   ├── StatusPage.vue     # Дашборд статуса сервиса
│   │   └── TemplateItemsDemo.vue
│   ├── ParentLayout.vue
│   ├── package.json           # @ergo-ms/module-template
│   ├── scss/
│   └── assets/
│       └── svg/
│           └── sdb.svg
├── ergoms.conf
├── ergoms.help.yaml
├── HOWTO.md
└── README.md
```

Краткое описание ключевых элементов:

- `HealthViewSet` в `api/views.py` — агрегированный статус сервиса, БД и демо‑метрики; доступ — `CanViewModuleTemplate`.
- `TemplateItemViewSet` — CRUD по `public_id`, `AuditedModelMixin`, `RequiresSessionScope`.
- `ml_service.py` — rule‑based классификатор текста.
- `MainPage.vue` / `StatusPage.vue` — UI через `$t('module_template.*')`.

---

## 2. Как запустить и посмотреть модуль

Все операции выполняются только через `ergoms`.

### Применить миграции модуля

```bash
ergoms module_template:migrate
```

### Запустить сервер и клиент (общие команды проекта)

```bash
ergoms dev
ergoms start-client
```

После запуска:

1. Откройте главную страницу модуля (пункт меню «Шаблон модуля» / `ModuleTemplateMain`).
2. Протестируйте ML‑демо: выберите один из быстрых примеров текста или введите свой и нажмите «Классифицировать».
3. Перейдите по кнопке «Мониторинг сервиса» на `StatusPage.vue` и посмотрите на демо‑метрики и графики.

Для доступа нужны право `module_template_view` (или роль глобального администратора).

---

## 3. Основные API‑эндпоинты

### Health‑check и метрики

`GET /api/module_template/health/`

Ответ всегда `200 OK`, статус кодируется в теле:

```json
{
  "status": "ok",
  "db": "ok",
  "time": "2026-03-16T12:00:00Z",
  "app_version": "dev",
  "latency_ms": 42.1,
  "requests_per_minute": 23.5,
  "error_rate": 0.7,
  "uptime_seconds": 12345,
  "environment": "development",
  "node_name": "node-1"
}
```

Эти данные визуализируются на `StatusPage.vue` (карточки статуса, графики, журнал измерений).

### ML‑модель (demo)

- `GET /api/module_template/model-meta/` — мета‑информация о модели.
- `POST /api/module_template/predict/` — классификация текста:

```json
{
  "text": "Критическая ошибка в production..."
}
```

Ответ содержит `category`, `priority`, `score`, `matched_keywords`, длину текста и число предложений. Эти данные отображаются на `MainPage.vue`.

Пути на клиенте — в `client/js/endpoints.js`.

### CRUD по TemplateItem

Базовый пример CRUD через DRF `ModelViewSet` (lookup — `public_id`):

- `GET /api/module_template/items/`
- `POST /api/module_template/items/`
- `GET /api/module_template/items/{public_id}/` и т.д.

Поддерживается фильтрация по признаку активности:

```text
/api/module_template/items/?active=true
```

Создание / изменение / удаление пишутся в журнал действий (`AuditedModelMixin`).

---

## 4. Клиентские маршруты

| Путь | Роут | Описание |
|------|------|----------|
| `/module-template` | `ModuleTemplate` → redirect | Оболочка, редирект на статус |
| `/module-template` (child `''`) | `ModuleTemplateMain` | Главная страница модуля |
| `/module-template/status` | `ModuleTemplateStatus` | Дашборд статуса и метрик |
| `/module-template/org-example` | `ModuleTemplateOrgExample` | Пример `requiresSessionScope` |

Заголовки маршрутов — `meta.titleKey` (`module_template.routes.*`). Навигация — `client/js/routes.js`; пункты бокового меню — миграция `api/migrations/0004_add_menu.py`.

---

## 5. Архитектура client‑части

### Composables

- `useModuleTemplateStatus` (`client/js/useModuleTemplate.js`) — health‑эндпоинт, история измерений, уровни `ok/warn/crit`, даты через `timeUtils`.
- `useModuleTemplateML` (`client/js/useModuleTemplateML.js`) — `model-meta` и `predict`.

### i18n

Все UI‑строки модуля — в `client/js/locales.js` (namespace `module_template`, языки `ru` и `en`). Подхват — `LocaleManager` ядра.

### Стили и тема

Стили используют Bootstrap / UI‑переменные (`--bs-*`, `--ui-*`). Отдельная модульная палитра (`theme-defaults.js`) не нужна.

---

## 6. Где смотреть how‑to сценарии

Для практических сценариев см. файл `HOWTO.md` в корне модуля. В нём разобраны:

- как заменить rule‑based модель на свою ML‑модель;
- как добавить новую метрику в health‑check и вывести её на `StatusPage.vue`;
- как добавить новую страницу/карточку на клиенте;
- platform‑контракты ModuleBridge.

---

## 7. Соглашения об импортах

**API (Python):**

- внутри модуля — относительные импорты (`from .models import TemplateItem`);
- из ядра — полные пути (`from src.core...`).

**Client (JavaScript/Vue):**

- из ядра — абсолютные пути (`import { apiClient } from '@/js/api/manager'`);
- внутри модуля — относительные пути (`import { moduleTemplateEndpoints } from '../js/endpoints'`).

---

## 8. Как расширять модуль

### Новые страницы на клиенте

1. Создайте компонент в `client/components/`.
2. Добавьте маршрут в `client/js/routes.js` (component — строка `@/modules/module_template/...`, `meta.titleKey`).
3. Добавьте ключи в `client/js/locales.js`.
4. Добавьте пункт в боковое меню через миграцию API (`MenuMigrationHelper`).
5. Вынесите стили в новый SCSS‑файл в `client/scss/`.

### Новые API‑эндпоинты

1. Добавьте `ViewSet` или `APIView` в `api/views.py` с `CanViewModuleTemplate` (или более узким правом).
2. Зарегистрируйте его в `api/urls.py`.
3. Опишите эндпоинт в `client/js/endpoints.js`.

### Celery‑задачи (опционально)

1. Создайте `api/tasks.py` с задачами.
2. Опишите очереди в `api/celery_config.py` и, при необходимости, периодические задания в `api/celery_beat_config.py`.

Более детальные примеры см. в `HOWTO.md`.
