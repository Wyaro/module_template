/**
 * Federation / standalone entry для module_template.
 * Экспортирует единый клиентский манифест (см. clientModuleManifest.js).
 *
 * Компоненты — lazy functions (не строковые пути), чтобы remote
 * не зависел от host glob `@/modules/...`.
 */

import routesConfig from './js/routes.js'
import { moduleTemplateEndpoints } from './js/endpoints.js'
import permissionRules from './js/permission-rules.js'
import routeGuard from './js/routeGuard.js'
import locales from './js/locales.js'
import './js/integrations.js'

function withLazyComponents(routes) {
  if (!routes || typeof routes !== 'object') {
    return routes
  }
  const out = {}
  for (const [name, cfg] of Object.entries(routes)) {
    out[name] = mapRoute(cfg)
  }
  return out
}

function mapRoute(cfg) {
  if (!cfg || typeof cfg !== 'object') {
    return cfg
  }
  const next = { ...cfg }
  if (typeof cfg.component === 'string') {
    next.component = resolveComponent(cfg.component)
  }
  if (Array.isArray(cfg.children)) {
    next.children = cfg.children.map((child) => mapRoute(child))
  } else if (cfg.children && typeof cfg.children === 'object') {
    next.children = Object.fromEntries(
      Object.entries(cfg.children).map(([k, v]) => [k, mapRoute(v)]),
    )
  }
  return next
}

/**
 * Строковые пути шаблона → lazy import относительно client/.
 * @param {string} componentPath
 */
function resolveComponent(componentPath) {
  const normalized = String(componentPath || '').replace(/\\/g, '/')
  if (normalized.endsWith('ParentLayout.vue')) {
    return () => import('./ParentLayout.vue')
  }
  if (normalized.includes('MainPage.vue')) {
    return () => import('./components/MainPage.vue')
  }
  if (normalized.includes('StatusPage.vue')) {
    return () => import('./components/StatusPage.vue')
  }
  return () => import('./ParentLayout.vue')
}

const manifest = {
  moduleKey: 'module_template',
  routes: withLazyComponents(routesConfig),
  endpoints: moduleTemplateEndpoints,
  permissionRules,
  routeGuard,
  locales,
}

export default manifest
export { manifest }

if (typeof globalThis !== 'undefined') {
  globalThis.__ERGO_MODULE_REMOTES__ = globalThis.__ERGO_MODULE_REMOTES__ || {}
  globalThis.__ERGO_MODULE_REMOTES__.module_template = manifest
}
