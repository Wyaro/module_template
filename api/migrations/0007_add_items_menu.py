from django.db import migrations


def add_items_menu(apps, schema_editor):
    from src.core.cms.adp.menu.migration_utils import MenuMigrationHelper

    helper = MenuMigrationHelper(apps, 'modules/module_template')
    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    parent = MenuItem.objects.filter(
        module_source='modules/module_template',
        route_name='ModuleTemplate',
        parent__isnull=True,
    ).first()
    if parent is None:
        return
    if MenuItem.objects.filter(
        module_source='modules/module_template',
        route_name='ModuleTemplateItems',
    ).exists():
        return
    helper.create_routes_batch(
        [('Элементы', 'ModuleTemplateItems', 'List')],
        parent=parent,
    )


def remove_items_menu(apps, schema_editor):
    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    MenuItem.objects.filter(
        module_source='modules/module_template',
        route_name='ModuleTemplateItems',
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('module_template', '0006_menu_shell_route'),
        ('cms_adp', '0007_populate_core_menu'),
    ]

    operations = [
        migrations.RunPython(add_items_menu, remove_items_menu),
    ]
