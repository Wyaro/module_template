# HOWTO: учебные сценарии для module_template

Этот файл собирает короткие практические сценарии по развитию модуля. Он дополняет `README.md` и отсылает к конкретным файлам в API и клиенте.

---

## 1. Заменить rule‑based модель на свою ML‑модель

**Цель:** использовать свой классификатор текста (sklearn / PyTorch / внешний сервис), сохранив существующий API‑контракт.

### Шаги

1. Откройте `[modules/module_template/api/ml_service.py](modules/module_template/api/ml_service.py)`.
2. Оставьте сигнатуру функции:

   ```python
   def predict(payload: Dict) -> Dict: ...
   ```

   и возвращаемую структуру (ключи `category`, `priority`, `score`, `matched_keywords`, `text_length`, `sentence_count`), чтобы клиент не пришлось менять.

3. Вместо вызова `_classify(text[:2000])`:

   - загрузите свою модель (например, в модуле‑одиночке или через lazy‑инициализацию),
   - подготовьте признаки (vectorizer, tokenizer и т.п.),
   - получите предсказание и переведите его в те же поля (`category`, `priority`, `score`).

4. В `get_model_meta()` обновите:

   - `model_name`, `model_version`, `model_type`,
   - по желанию добавьте дополнительные поля (например, размер датасета, используемую архитектуру).

Клиент (`MainPage.vue` + `useModuleTemplateML.js`) автоматически подхватит новые значения без изменений, если структура ответа сохранена.

---

## 2. Добавить новую метрику в health‑check и вывести её на StatusPage

**Цель:** расширить демонстрационный мониторинг своей метрикой (например, `queue_size` или `cpu_load`).

### Шаги на сервере

1. Откройте `[modules/module_template/api/views.py](modules/module_template/api/views.py)` и функцию `_demo_metrics()`.
2. Добавьте новую метрику в словарь, например:

   ```python
   def _demo_metrics() -> dict:
       return {
           "latency_ms": ...,
           "requests_per_minute": ...,
           "error_rate": ...,
           "queue_size": random.randint(0, 50),
           ...
       }
   ```

3. Убедитесь, что ключ входит в `response_data`, возвращаемый методом `health`.

### Шаги на клиенте

1. В composable `[modules/module_template/client/js/useModuleTemplate.js](modules/module_template/client/js/useModuleTemplate.js)`:

   - добавьте поле в `statusData` и объекты, которые пишутся в `history`;
   - при необходимости добавьте агрегаты (средние значения) в `metricAggregates`.

2. В компоненте `[modules/module_template/client/components/StatusPage.vue](modules/module_template/client/components/StatusPage.vue)`:

   - создайте ещё одну metric‑карточку или включите метрику в существующие;
   - определите уровни `ok/warn/crit` через `ALERT_THRESHOLDS` и `getAlertLevel`.

3. Добавьте подписи в `client/js/locales.js` (ru и en) и обновите стили в `status-page.scss` при необходимости.

---

## 3. Добавить новую страницу / карточку на клиенте

**Цель:** показать типичный путь от маршрута до компонента и меню.

### Шаги

1. Создайте Vue‑компонент, например `client/components/ExamplesPage.vue`. Строки UI — через `useI18n()` и ключи `module_template.*`.
2. Добавьте ключи заголовка в `[modules/module_template/client/js/locales.js](modules/module_template/client/js/locales.js)`.
3. Добавьте дочерний маршрут в `[modules/module_template/client/js/routes.js](modules/module_template/client/js/routes.js)`:

   ```javascript
   {
     path: 'examples',
     name: 'ModuleTemplateExamples',
     component: '@/modules/module_template/client/components/ExamplesPage.vue',
     meta: {
       titleKey: 'module_template.routes.examples',
     },
   }
   ```

   Component — **строка пути** для lazy‑load через RouteManager ядра (не sync `import` и не `() => import(...)` с относительным путём в устаревшем стиле).

4. Добавьте пункт меню через миграцию API (`MenuMigrationHelper`, эталон — `api/migrations/0004_add_menu.py`).
5. При необходимости создайте файл стилей `client/scss/examples-page.scss` и подключите его внутри компонента:

   ```vue
   <style lang="scss" scoped>
   @import '../scss/examples-page.scss';
   </style>
   ```

---

## 4. Права и аудит (эталон)

**Цель:** сервер проверяет права сам; клиентский `permission-rules.js` — только UX.

1. Ключ права — в `api/permissions.py` (`TEMPLATE_VIEW` / `CanViewModuleTemplate`).
2. Каталог для ADP — `api/permission_catalog.py`.
3. ViewSet / ViewSet actions — `permission_classes = [IsAuthenticated, CanViewModuleTemplate, ...]`.
4. CRUD с журналом — `AuditedModelMixin` + действия в `api/integrations.py` (`AUDIT_ACTION_DEFINITIONS_GROUP`).
5. Клиент — `client/js/permission-rules.js` с теми же ключами в `permissions`.

---

## 5. Platform-контракты модуля

**Цель:** подключить только нужные контракты ModuleBridge без import из других модулей.

Полный каталог — [`.cursor/rules/module-contracts.mdc`](../../.cursor/rules/module-contracts.mdc). В `module_template` уже есть stub:

| Контракт | Файл |
|----------|------|
| `audit.action_definitions`, `core.user_delete` | [`api/integrations.py`](api/integrations.py) |
| `layout.plugin_registry` | [`client/js/integrations.js`](client/js/integrations.js) |
| `routeGuard` (passthrough) | [`client/js/routeGuard.js`](client/js/routeGuard.js) |
| Sidebar CMS | [`api/migrations/0004_add_menu.py`](api/migrations/0004_add_menu.py) |

Чеклист при новом модуле:

1. Нужен session-scoped UI (организация и т.п.) — `meta.requiresSessionScope` + при необходимости `SESSION_SCOPED_MODULE_CONTEXT_GROUP` / `RequiresSessionScope` на API.
2. Нужен audit — секция в `api/integrations.py` через `AUDIT_ACTION_DEFINITIONS_GROUP`.
3. Нужна очистка при удалении user — `@bridge.subscribe_to(CORE_USER_DELETE)`.
4. Нужен sidebar — миграция меню по образцу `0004_add_menu.py`.

---

## 6. Полезные команды ergoms для работы с модулем

```bash
# Применить миграции модуля
ergoms module_template:migrate

# Запустить API (dev)
ergoms dev

# Запустить клиент (Vue dev)
ergoms start-client
```

Для полного списка команд по проекту используйте:

```bash
ergoms help
```
