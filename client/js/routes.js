export default {
  ModuleTemplate: {
    path: '/module-template',
    name: 'ModuleTemplate',
    redirect: { name: 'ModuleTemplateStatus' },
    component: '@/modules/module_template/client/ParentLayout.vue',
    meta: {
      titleKey: 'module_template.routes.shell',
      requiresAuth: true,
    },
    children: [
      {
        path: '',
        name: 'ModuleTemplateMain',
        component: '@/modules/module_template/client/components/MainPage.vue',
        meta: {
          titleKey: 'module_template.routes.main',
        },
      },
      {
        path: 'status',
        name: 'ModuleTemplateStatus',
        component: '@/modules/module_template/client/components/StatusPage.vue',
        meta: {
          titleKey: 'module_template.routes.status',
        },
      },
      {
        path: 'patterns',
        name: 'ModuleTemplatePatterns',
        component: '@/modules/module_template/client/components/PatternsPage.vue',
        meta: {
          titleKey: 'module_template.routes.patterns',
        },
      },
    ],
  },
}
