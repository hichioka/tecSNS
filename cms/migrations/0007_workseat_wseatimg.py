# Generated by Django 3.1.1 on 2020-10-21 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_remove_workseat_wseatimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='workseat',
            name='Wseatimg',
            field=models.FileField(default='', upload_to='images/', verbose_name='シートのデータ'),
        ),
    ]
