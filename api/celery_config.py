"""Очереди Celery для module_template (эталон для копирования)."""

from typing import Any, Dict

from src.core.utils.celery.base import CeleryModuleConfig


class ModuleTemplateCeleryConfig(CeleryModuleConfig):
    def get_task_routes(self) -> Dict[str, Dict[str, Any]]:
        return {
            'modules.module_template.api.tasks.*': {'queue': 'module_template'},
        }

    def get_task_queues(self) -> Dict[str, Dict[str, Any]]:
        return {
            'module_template': {
                'exchange': 'module_template',
                'routing_key': 'module_template',
            },
        }

    def get_task_annotations(self) -> Dict[str, Dict[str, Any]]:
        return {}
