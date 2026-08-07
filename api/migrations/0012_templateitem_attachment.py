from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_template', '0011_menu_modules_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateitem',
            name='attachment',
            field=models.FileField(
                blank=True,
                max_length=512,
                null=True,
                upload_to='module_template/attachments/',
            ),
        ),
    ]
