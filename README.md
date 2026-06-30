# Module Template (module_template)

Учебный модуль для системы ERGO MS. Показывает, как в одном месте собрать:

- health‑check и мониторинг сервиса,
- простую rule‑based «ML‑модель»,
- типовой CRUD‑API и Vue‑интерфейс.

Модуль задуман как отправная точка для студенческих и исследовательских модулей СКБ.

---

## 1. Структура модуля

```text
modules/module_template/
├── api/                       # Серверная часть (Django + DRF)
│   ├── apps.py                # AppConfig модуля
│   ├── config.py              # Константы (MODULE_DATABASE_ALIAS, VERSION, USE_GPU)
│   ├── models.py              # Модель TemplateItem (пример CRUD-сущности)
│   ├── serializers.py         # TemplateItemSerializer
│   ├── views.py               # TemplateItemViewSet, HealthViewSet, ML endpoints
│   ├── ml_service.py          # Rule-based модель для текста (demo)
│   ├── routers.py             # Маршрутизация БД (по умолчанию alias `default`)
│   ├── urls.py                # URL-маршруты модуля
│   └── migrations/
├── client/                    # Клиентская часть (Vue)
│   ├── js/
│   │   ├── routes.js          # Маршруты Vue Router
│   │   ├── menu-config.json   # Пункты меню в ядре
│   │   ├── endpoints.js       # Эндпоинты API модуля
│   │   ├── useModuleTemplate.js   # Health‑check и метрики
│   │   └── useModuleTemplateML.js # Работа с ML‑эндпоинтами
│   ├── components/
│   │   ├── MainPage.vue       # Главный экран модуля СКБ
│   │   └── StatusPage.vue     # Дашборд статуса сервиса
│   ├── scss/
│   │   ├── main-page.scss     # Стили главной страницы
│   │   └── status-page.scss   # Стили страницы статуса
│   └── assets/
│       └── svg/
│           └── sdb.svg        # Эмблема «Студенческого конструкторского бюро»
├── ergoms.conf                # Команды ergoms для модуля
└── README.md
```

Краткое описание ключевых элементов:

- `HealthViewSet` в `api/views.py` — возвращает агрегированный статус сервиса, БД и демо‑метрики, всегда с кодом `200 OK`, а реальное состояние — в JSON.
- `ml_service.py` — rule‑based классификатор текста: категория, приоритет, балл важности и сработавшие ключевые слова.
- `MainPage.vue` — академичный обзор модуля + интерактивное ML‑демо.
- `StatusPage.vue` — учебный пример мониторинга: метрики, графики, журнал измерений.

---

## 2. Как запустить и посмотреть модуль

Все операции выполняются только через `ergoms`.

### Применить миграции модуля

```bash
ergoms module_template:migrate
```

### Запустить backend и клиент (общие команды проекта)

```bash
# Django API (dev)
ergoms dev

# Клиент (Vue dev)
ergoms start-client
```

После запуска:

1. Откройте главную страницу модуля (пункт меню «Шаблон модуля» / `ModuleTemplateMain`).
2. Протестируйте ML‑демо: выберите один из быстрых примеров текста или введите свой и нажмите «Классифицировать».
3. Перейдите по кнопке «Мониторинг сервиса» на `StatusPage.vue` и посмотрите на демо‑метрики и графики.

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

- `GET /api/module_template/health/model-meta/` — мета‑информация о модели (тип, версия, поддерживаемые категории, подсказка по замене).
- `POST /api/module_template/health/predict/` — классификация текста:

```json
{
  "text": "Критическая ошибка в production..."
}
```

Ответ содержит `category`, `priority`, `score`, `matched_keywords`, длину текста и число предложений. Эти данные отображаются на `MainPage.vue`.

### CRUD по TemplateItem

Базовый пример CRUD через DRF `ModelViewSet`:

- `GET /api/module_template/items/`
- `POST /api/module_template/items/`
- `GET /api/module_template/items/{id}/` и т.д.

Поддерживается фильтрация по признаку активности:

```text
/api/module_template/items/?active=true
```

---

## 4. Клиентские маршруты

| Путь                        | Роут                | Описание                       |
|-----------------------------|---------------------|--------------------------------|
| `/module-template`         | `ModuleTemplateMain` | Главная страница модуля       |
| `/module-template/status`  | `ModuleTemplateStatus` | Дашборд статуса и метрик   |

Навигация и пункты меню модуля описаны в `client/js/routes.js` и `client/js/menu-config.json` и автоматически подхватываются ядром.

---

## 5. Архитектура client‑части

### Composables

- `useModuleTemplateStatus` (`client/js/useModuleTemplate.js`) — обращается к `health`‑эндпоинту, ведёт историю измерений, вычисляет уровни `ok/warn/crit`.
- `useModuleTemplateML` (`client/js/useModuleTemplateML.js`) — работает с `model-meta` и `predict`, обрезает слишком длинные тексты и отдаёт данные в `MainPage.vue`.

### Стили и тема

Стили главной и статус‑страницы вынесены в SCSS‑файлы и используют только Bootstrap‑переменные (`--bs-*`), чтобы модуль выглядел единым с ядром:

```vue
<style lang="scss" scoped>
@import '../scss/main-page.scss';
</style>
```

Аналогично для `status-page.scss`.

---

## 6. Где смотреть how‑to сценарии

Для практических сценариев см. файл `HOWTO.md` в корне модуля. В нём разобраны:

- как заменить rule‑based модель на свою ML‑модель;
- как добавить новую метрику в health‑check и вывести её на `StatusPage.vue`;
- как добавить новую страницу/карточку на клиенте.

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
2. Добавьте маршрут в `client/js/routes.js`.
3. При необходимости добавьте пункт в меню в `client/js/menu-config.json`.
4. Вынесите стили в новый SCSS‑файл в `client/scss/`.

### Новые API‑эндпоинты

1. Добавьте `ViewSet` или `APIView` в `api/views.py`.
2. Зарегистрируйте его в `api/urls.py`.
3. Опишите эндпоинт в `client/js/endpoints.js` и используйте его из composable или компонента.

### Celery‑задачи (опционально)

1. Создайте `api/tasks.py` с задачами.
2. Опишите очереди в `api/celery_config.py` и, при необходимости, периодические задания в `api/celery_beat_config.py`.

Более детальные примеры см. в `HOWTO.md`.
