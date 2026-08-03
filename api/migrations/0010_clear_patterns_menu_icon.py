# -*- coding: utf-8 -*-
"""Убрать иконку у пункта меню ModuleTemplatePatterns."""

from django.db import migrations


def clear_patterns_icon(apps, schema_editor):
    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    MenuItem.objects.filter(
        module_source='modules/module_template',
        route_name='ModuleTemplatePatterns',
    ).update(icon=None)


def restore_patterns_icon(apps, schema_editor):
    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    MenuItem.objects.filter(
        module_source='modules/module_template',
        route_name='ModuleTemplatePatterns',
    ).update(icon='LayoutTemplate')


class Migration(migrations.Migration):

    dependencies = [
        ('module_template', '0009_add_patterns_menu'),
    ]

    operations = [
        migrations.RunPython(clear_patterns_icon, restore_patterns_icon),
    ]
