/**
 * Route guard модуля.
 *
 * Platform session-scope (meta.requiresSessionScope) уже проверяет ядро
 * в routers.js через runSessionScopeGuard. Здесь — только доменная логика
 * (например validateSession API владельца scope).
 *
 * Эталон владельца scope: modules/<host_module>/client/js/*Guard.js
 */

export async function routeGuard(_to, _from, next) {
  return next()
}

export default routeGuard
