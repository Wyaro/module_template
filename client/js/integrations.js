/**
 * ModuleBridge client — учебные stub-контракты module_template.
 *
 * Session-scope (gating claim, welcome, module_context) регистрирует
 * модуль-владелец домена (<host_module>), не этот шаблон.
 */

import bridge from '@/integrations/ModuleBridge.js'
import { LAYOUT_PLUGIN_REGISTRY_GROUP } from '@/integrations/moduleContracts.js'
// import { SESSION_SCOPED_MODULE_CONTEXT_GROUP } from '@/integrations/moduleContracts.js'
// import { SESSION_SCOPE_GATING_CLAIM_GROUP } from '@/integrations/sessionScopeGating.js'

bridge.provideMany(LAYOUT_PLUGIN_REGISTRY_GROUP, 'module_template', {
  routeNamePrefixes: ['ModuleTemplate'],
})

// --- Session-scope (эталон, выключен) -----------------------------------------
// bridge.provideMany(SESSION_SCOPED_MODULE_CONTEXT_GROUP, 'module_template', {
//   pathPrefix: '/module-template',
//   homeRoute: 'ModuleTemplateMain',
// })
// bridge.provideMany(SESSION_SCOPE_GATING_CLAIM_GROUP, 'my_scope', 'my_scope_id')
// ------------------------------------------------------------------------------
