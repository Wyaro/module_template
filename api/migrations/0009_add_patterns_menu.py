# -*- coding: utf-8 -*-
"""Пункт меню «Паттерны ядра» → ModuleTemplatePatterns."""

from django.db import migrations


def add_patterns_menu(apps, schema_editor):
    from src.core.cms.adp.menu.migration_utils import MenuMigrationHelper

    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    helper = MenuMigrationHelper(apps, 'modules/module_template')

    parent = MenuItem.objects.filter(
        module_source='modules/module_template',
        parent__isnull=True,
    ).first()

    helper.create_route(
        'Паттерны ядра',
        'ModuleTemplatePatterns',
        parent=parent,
    )


def remove_patterns_menu(apps, schema_editor):
    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    MenuItem.objects.filter(
        module_source='modules/module_template',
        route_name='ModuleTemplatePatterns',
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('module_template', '0008_remove_items_menu'),
        ('cms_adp', '0001_initial_squashed_0042_drop_graduate_employment_tables'),
    ]

    operations = [
        migrations.RunPython(add_patterns_menu, remove_patterns_menu),
    ]
