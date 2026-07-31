# module_template — инструкции агенту

Учебный модуль ERGO MS: health/ML-демо, CRUD `TemplateItem`, клиент на компонентах ядра.

## Куда смотреть

- Структура и запуск — `README.md`, сценарии — `HOWTO.md`
- Правила Cursor модуля — `.cursor/rules/` (подхватывает расширение ERGO MS Module Cursor Rules)
- Платформа ядра — корневые `.cursor/rules/` (isolation, ModuleBridge, SelectBox, security)

## Запрещено

- pk БД в URL / storage — только `public_id`
- Свой `<select>` вместо `SelectBox` ядра
- Прямой import домена модуля из `core/`
- Команды мимо `ergoms`

## Команды

```bash
ergoms module_template:migrate
ergoms dev
ergoms start-client
```
