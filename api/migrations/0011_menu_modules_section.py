# -*- coding: utf-8 -*-
"""Корневой пункт шаблона — в секцию «Модули» (order >= 20)."""

from django.db import migrations


def move_menu_to_modules_section(apps, schema_editor):
    from src.core.cms.adp.menu.migration_utils import align_module_root_menu_orders

    align_module_root_menu_orders(apps, 'modules/module_template')


class Migration(migrations.Migration):

    dependencies = [
        ('module_template', '0010_clear_patterns_menu_icon'),
        ('cms_adp', '0054_menu_catalog_layout'),
    ]

    operations = [
        migrations.RunPython(move_menu_to_modules_section, migrations.RunPython.noop),
    ]
