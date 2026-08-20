from django.db import models

from src.core.utils.base.models import PublicIdMixin


class TemplateItem(PublicIdMixin, models.Model):
    name = models.CharField(max_length=255, default='Без названия', blank=True, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    # Файл только через media_api (path в FileField.name); не раздавать с основного API.
    attachment = models.FileField(
        upload_to='module_template/attachments/',
        blank=True,
        null=True,
        max_length=512,
    )

    class Meta:
        app_label = 'module_template'
        verbose_name = 'Template Item'
        verbose_name_plural = 'Template Items'

    def __str__(self):
        return self.name
