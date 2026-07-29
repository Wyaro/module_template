from django.db import migrations


def remove_items_menu(apps, schema_editor):
    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    MenuItem.objects.filter(
        module_source='modules/module_template',
        route_name='ModuleTemplateItems',
    ).delete()


def noop_reverse(apps, schema_editor):
    # Пункт ModuleTemplateItems больше не используется — reverse пустой.
    return None


class Migration(migrations.Migration):
    dependencies = [
        ('module_template', '0007_add_items_menu'),
        ('cms_adp', '0007_populate_core_menu'),
    ]

    operations = [
        migrations.RunPython(remove_items_menu, noop_reverse),
    ]
