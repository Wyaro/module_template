/**
 * Правила проверки прав для module_template (UX).
 * titleKey / messageKey — ключи i18n; сервер всё равно проверяет сам.
 */
export default [
  {
    match: (to) =>
      to.name?.toString().startsWith('ModuleTemplate') ||
      to.path?.startsWith('/module-template'),
    module: 'module_template',
    permissions: ['module_template_view'],
    titleKey: 'module_template.access.title',
    messageKey: 'module_template.access.message',
  },
]
