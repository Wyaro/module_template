/**
 * ModuleBridge client — учебные stub-контракты module_template.
 */

import bridge from '@/integrations/ModuleBridge.js'
import { LAYOUT_PLUGIN_REGISTRY_GROUP } from '@/integrations/moduleContracts.js'

bridge.provideMany(LAYOUT_PLUGIN_REGISTRY_GROUP, 'module_template', {
  routeNamePrefixes: ['ModuleTemplate'],
})
