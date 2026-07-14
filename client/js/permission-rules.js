/**
 * Правила проверки прав для module_template (UX).
 */
export default [
  {
    match: (to) =>
      to.name?.toString().startsWith('ModuleTemplate') ||
      to.path?.startsWith('/module-template'),
    module: 'module_template',
    permissions: ['module_template_view'],
    title: 'Доступ к шаблону модуля ограничен',
    message: 'У вас нет прав для просмотра учебного модуля. Обратитесь к администратору.',
  },
]
