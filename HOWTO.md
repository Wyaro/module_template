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

   и возвращаемую структуру (ключи `category`, `priority`, `score`, `matched_keywords`, `text_length`, `sentence_count`), чтобы фронт не пришлось менять.

3. Вместо вызова `_classify(text[:2000])`:

   - загрузите свою модель (например, в модуле‑одиночке или через lazy‑инициализацию),
   - подготовьте признаки (vectorizer, tokenizer и т.п.),
   - получите предсказание и переведите его в те же поля (`category`, `priority`, `score`).

4. В `get_model_meta()` обновите:

   - `model_name`, `model_version`, `model_type`,
   - по желанию добавьте дополнительные поля (например, размер датасета, используемую архитектуру).

Фронтенд (`MainPage.vue` + `useModuleTemplateML.js`) автоматически подхватит новые значения без изменений, если структура ответа сохранена.

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

3. Обновите подсказки в `status-page.scss` и/или текстовые подписи, чтобы студенту было понятно, что именно показывает новая метрика.

---

## 3. Добавить новую страницу / карточку на клиенте

**Цель:** показать студентам типичный путь от маршрута до компонента и меню.

### Шаги

1. Создайте Vue‑компонент, например `client/components/ExamplesPage.vue`.
2. Добавьте маршрут в `[modules/module_template/client/js/routes.js](modules/module_template/client/js/routes.js)`:

   ```javascript
   {
     path: '/module-template/examples',
     name: 'ModuleTemplateExamples',
     component: () => import('../components/ExamplesPage.vue'),
     meta: { title: 'Примеры', requiresAuth: true },
   }
   ```

3. Добавьте пункт меню через миграцию API (`MenuMigrationHelper`, эталон — `api/migrations/0004_add_menu.py`), чтобы страница появилась в навигации.
4. При необходимости создайте файл стилей `client/scss/examples-page.scss` и подключите его внутри компонента через:

   ```vue
   <style lang="scss" scoped>
   @import '../scss/examples-page.scss';
   </style>
   ```

---

## 4. Полезные команды ergoms для работы с модулем

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

