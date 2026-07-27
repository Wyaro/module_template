# -*- coding: utf-8 -*-
"""Корневой пункт меню шаблона → routeName ModuleTemplate (titleKey shell)."""

from django.db import migrations


def fix_menu_shell_route(apps, schema_editor):
    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    MenuItem.objects.filter(
        module_source='modules/module_template',
        parent__isnull=True,
        route_name='ModuleTemplateMain',
    ).update(route_name='ModuleTemplate')


def restore_menu_shell_route(apps, schema_editor):
    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    MenuItem.objects.filter(
        module_source='modules/module_template',
        parent__isnull=True,
        route_name='ModuleTemplate',
    ).update(route_name='ModuleTemplateMain')


class Migration(migrations.Migration):

    dependencies = [
        ('module_template', '0005_templateitem_public_id'),
    ]

    operations = [
        migrations.RunPython(fix_menu_shell_route, restore_menu_shell_route),
    ]
