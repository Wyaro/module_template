/**
 * Опциональный route guard модуля — passthrough по умолчанию.
 */

export async function routeGuard(_to, _from, next) {
  return next()
}

export default routeGuard
