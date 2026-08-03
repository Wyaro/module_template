# module_template — инструкции агенту

**Живой шаблон** ERGO MS: health/ML, CRUD `TemplateItem`, каталог паттернов ядра.

Новый переиспользуемый функционал ядра для модулей **обязан** иметь демо здесь (`core_patterns.json` + UI) — см. `.cursor/rules/module-template-living.mdc`.

## Куда смотреть

- Роль шаблона — `.cursor/rules/module-template-living.mdc`
- Структура кода — `.cursor/rules/module-template.mdc`
- Каталог эталонов — `client/js/core_patterns.json`, страница `PatternsPage.vue`
- Сценарии — `HOWTO.md`, обзор — `README.md`
- Платформа ядра — корневые `.cursor/rules/`

## Запрещено

- pk БД в URL / storage — только `public_id`
- Свой `<select>` вместо `SelectBox`
- Сырые `form-label` в модалках вместо `FormCard`/`FormField`
- Прямой `useI18n` — только `useAppI18n`
- Паттерн ядра «для модулей» без демо и записи в `core_patterns.json`
- Прямой import домена модуля из `core/`
- Команды мимо `ergoms`

## Команды

```bash
ergoms module_template:patterns-check
ergoms module_template:migrate
ergoms dev
ergoms start-client
```
