from uuid import uuid4

from django.db import models


class TemplateItem(models.Model):
    public_id = models.UUIDField(default=uuid4, unique=True, editable=False, db_index=True)
    name = models.CharField(max_length=255, default='Без названия', blank=True, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = 'module_template'
        verbose_name = 'Template Item'
        verbose_name_plural = 'Template Items'

    def __str__(self):
        return self.name
