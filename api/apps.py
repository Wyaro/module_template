from django.apps import AppConfig


class ModuleTemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.module_template.api'
    label = 'module_template'
    verbose_name = 'Module Template'

    def ready(self):
        from . import integrations  # noqa: F401
