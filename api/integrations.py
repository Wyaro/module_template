"""ModuleBridge — учебные stub-контракты для module_template."""

from __future__ import annotations

from typing import Any, Dict

from src.core.integrations import bridge
from src.core.integrations.module_contracts import (
    AUDIT_ACTION_DEFINITIONS_GROUP,
    CORE_USER_DELETE,
    MEDIA_UPLOAD_QUOTA_POLICIES_GROUP,
    # SESSION_CLAIMS_GROUP,  # раскомментируйте для session-scoped модуля
)
from src.core.utils.media_upload_quota import (
    allows_module_permission,
    env_upload_rate,
)

from .ml_service import get_model_meta
from .permissions import MODULE_NAME, TEMPLATE_VIEW

# --- Session-scope (эталон, выключен) -----------------------------------------
# Регистрирует владелец scope (<host_module>), не каждый учебный модуль.
#
# from src.core.integrations.module_contracts import SESSION_CLAIMS_GROUP
#
# def _resolve_scope(*, my_scope_id, **kwargs):
#     ...
#
# bridge.provide_many(SESSION_CLAIMS_GROUP, 'my_scope', {
#     'claim': 'my_scope_id',
#     'request_attr': 'my_scope_id',
#     'entity_key': 'my_scope',
#     'resolve': _resolve_scope,
#     'required_guard': True,
# })
# ------------------------------------------------------------------------------


@bridge.provide_op('module_template.health_status')
def _health_status() -> Dict[str, Any]:
    return {
        'module': 'module_template',
        'model_meta': get_model_meta(),
    }


@bridge.provide_op('module_template.ping')
def _ping(*, echo: str = '') -> Dict[str, Any]:
    """JSON-only op для проверки BRIDGE_TRANSPORT=http между процессами."""
    return {
        'module': 'module_template',
        'pong': True,
        'echo': echo,
    }


bridge.provide_many(
    AUDIT_ACTION_DEFINITIONS_GROUP,
    key='module_template',
    obj={
        'module': 'module_template',
        'module_label': 'Шаблон модуля',
        'actions': [
            {
                'action': 'module_template.templateitem.created',
                'label': 'Элемент шаблона создан',
                'icon': 'Plus',
                'category': 'templateitem',
                'category_label': 'Элементы шаблона',
                'severity': 'info',
            },
            {
                'action': 'module_template.templateitem.updated',
                'label': 'Элемент шаблона изменён',
                'icon': 'Pencil',
                'category': 'templateitem',
                'category_label': 'Элементы шаблона',
                'severity': 'info',
            },
            {
                'action': 'module_template.templateitem.deleted',
                'label': 'Элемент шаблона удалён',
                'icon': 'Trash2',
                'category': 'templateitem',
                'category_label': 'Элементы шаблона',
                'severity': 'info',
            },
        ],
    },
)


@bridge.subscribe_to(CORE_USER_DELETE)
def _on_user_delete(**_kwargs: Any) -> None:
    """Stub: очистка данных модуля при удалении пользователя."""
    return None


bridge.provide_many(MEDIA_UPLOAD_QUOTA_POLICIES_GROUP, 'module_template', {
    'target_dir_prefix': 'module_template/',
    'quota': 'module_template',
    'rate': lambda: env_upload_rate('MODULE_TEMPLATE_UPLOAD_RATE', '30/minute'),
    'allows': allows_module_permission(MODULE_NAME, TEMPLATE_VIEW),
})
