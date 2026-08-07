# module_template — инструкции агенту

**Живой шаблон** ERGO MS: health/ML, CRUD `TemplateItem`, каталог паттернов ядра.

Новый переиспользуемый функционал ядра для модулей **обязан** иметь демо здесь (`core_patterns.json` + UI) — см. `.cursor/rules/module-template-living.mdc`. Документацию модуля держи в синхроне с кодом — корневой `module-docs.mdc`.

## Куда смотреть

- Роль шаблона — `.cursor/rules/module-template-living.mdc`
- Структура кода — `.cursor/rules/module-template.mdc`
- Каталог эталонов — `client/js/core_patterns.json`, страница `PatternsPage.vue`
- Оболочка UI — `client/scss/page-shell.scss` (`admin-page` / `page-header` / `content-card`)
- Сценарии — `HOWTO.md`, обзор — `README.md`
- Платформа ядра — корневые `.cursor/rules/`

## Запрещено

- pk БД в URL / storage — только `public_id`
- Свой `<select>` вместо `SelectBox`
- Bootstrap `btn btn-primary` в модалках — только `ui-btn ui-btn--primary|secondary`
- Сырые `form-label` в модалках вместо `FormCard`/`FormField`
- Свой page-shell с лишним padding / icon-pill вместо `page-header`
- Прямой `useI18n` — только `useAppI18n`
- Паттерн ядра «для модулей» без демо и записи в `core_patterns.json`
- Прямой import домена модуля из `core/`
- Команды мимо `ergoms`
- Файлы через `/media/` основного API — только media_api (`attachment_path` + `mediaApiClient`)
- Legacy query `search` для списка — канон `q`

## Обязательно

- Список TemplateItem — параметр поиска `q`
- Вложение TemplateItem — upload через `mediaApiClient`, API поле `attachment_path`, скачивание по signed URL
- Эталон пользовательской справки для RAG ai_assistant — `api/user_guides/*.md` и `user_description` в `permission_catalog.py`

## Команды

```bash
ergoms module_template:patterns-check
ergoms module_template:migrate
ergoms dev
ergoms start-client
```
