# Generated migration

import uuid

from django.db import migrations, models


def populate_public_id(apps, schema_editor):
    TemplateItem = apps.get_model('module_template', 'TemplateItem')
    for item in TemplateItem.objects.filter(public_id__isnull=True):
        item.public_id = uuid.uuid4()
        item.save(update_fields=['public_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('cms_adp', '0001_initial_squashed_0042_drop_graduate_employment_tables'),
        ('module_template', '0004_add_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateitem',
            name='public_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(populate_public_id, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='templateitem',
            name='public_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.RemoveField(
            model_name='templateitem',
            name='item_id',
        ),
    ]
