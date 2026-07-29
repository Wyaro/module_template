"""Учебная Celery-задача module_template (эталон для копирования)."""

from celery import shared_task


@shared_task(name='modules.module_template.api.tasks.ping')
def ping() -> str:
    """Минимальная задача — проверьте очередь ergoms start-worker."""
    return 'ok'
