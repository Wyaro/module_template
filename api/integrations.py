"""ModuleBridge — учебный stub для module_template."""

from __future__ import annotations

from typing import Any, Dict

from src.core.integrations import bridge

from .ml_service import get_model_meta


@bridge.provide_op('module_template.health_status')
def _health_status() -> Dict[str, Any]:
    return {
        'module': 'module_template',
        'model_meta': get_model_meta(),
    }
