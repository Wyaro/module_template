# -*- coding: utf-8 -*-
"""
Миграция данных: регистрация пунктов меню модуля module_template.
"""

from django.db import migrations


def add_menu(apps, schema_editor):
    from src.core.cms.adp.menu.migration_utils import MenuMigrationHelper

    helper = MenuMigrationHelper(apps, 'modules/module_template')
    helper.clear_module_items()

    root = helper.create_group('Шаблон модуля', 'ModuleTemplate', icon='Brain')
    helper.create_routes_batch([
        ('Главная', 'ModuleTemplateMain'),
        ('Статус сервиса', 'ModuleTemplateStatus'),
    ], parent=root)


def remove_menu(apps, schema_editor):
    from src.core.cms.adp.menu.migration_utils import MenuMigrationHelper

    helper = MenuMigrationHelper(apps, 'modules/module_template')
    helper.clear_module_items()


class Migration(migrations.Migration):

    dependencies = [
        ('module_template', '0003_templateitem'),
        ('cms_adp', '0001_initial_squashed_0042_drop_graduate_employment_tables'),
    ]

    operations = [
        migrations.RunPython(add_menu, remove_menu),
    ]
