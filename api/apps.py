from django.apps import AppConfig


class ModuleTemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.module_template.api'
    label = 'module_template'
    verbose_name = 'Module Template'
    # Зависимости модулей — modules/module_template/integrations.yaml (requires / extends).

    def ready(self):
        from . import integrations  # noqa: F401
