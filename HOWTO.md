# HOWTO: учебные сценарии для module_template

Этот файл дополняет `README.md` короткими практическими сценариями.

---

## 1. Заменить rule-based модель на свою ML-модель

1. Откройте [`api/ml_service.py`](api/ml_service.py).
2. Сохраните сигнатуру `predict(payload) -> dict` и ключи ответа.
3. Замените `_classify(...)` на вызов своей модели.
4. Обновите `get_model_meta()`.

Клиент (`MainPage.vue` + `useModuleTemplateML.js`) подхватит ответ при той же структуре.

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
- create/edit — `ModalCenter` (`defineAsyncComponent` + `v-if`);
- delete — `confirmDelete`;
- ключи API — `public_id`.

---

## 4. Права и аудит

1. Ключ права — `api/permissions.py` / `permission_catalog.py`.
2. ViewSet — `permission_classes = [IsAuthenticated, CanViewModuleTemplate, ...]`.
3. CRUD с журналом — `AuditedModelMixin` + `AUDIT_ACTION_DEFINITIONS_GROUP`.
4. UX-guard — `permission-rules.js` с `titleKey` / `messageKey`.

В шаблоне одно право `module_template_view` закрывает весь CRUD — в боевом модуле разделите права.

---

## 5. Platform-контракты ModuleBridge

Полный каталог — [`.cursor/rules/module-contracts.mdc`](../../.cursor/rules/module-contracts.mdc).

| Контракт | Файл |
|----------|------|
| `audit.action_definitions`, `core.user_delete` | [`api/integrations.py`](api/integrations.py) |
| `layout.plugin_registry` | [`client/js/integrations.js`](client/js/integrations.js) |
| stub session-scope (закомментирован) | те же integrations |
| `routeGuard` (passthrough) | [`client/js/routeGuard.js`](client/js/routeGuard.js) |
| Sidebar | миграции меню |

Session-scoped UI регистрирует владелец scope `<host_module>` (`SESSION_CLAIMS_GROUP` и клиентские группы). Эталон guard: `modules/<host_module>/client/js/*Guard.js`.

Межмодульные группы **не** кладите в каталог ядра. Platform-константы импортируйте из каталога ядра.

---

## 6. Celery

Эталон: [`api/tasks.py`](api/tasks.py), [`api/celery_config.py`](api/celery_config.py).

```bash
ergoms start-worker
```

---

## 7. Команды

```bash
ergoms module_template:migrate
ergoms dev
ergoms start-client
ergoms help
```
