# Generated by Django 4.1.1 on 2022-11-11 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spkapp', '0003_alter_projects_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_model',
            name='projectname',
            field=models.CharField(max_length=40),
        ),
    ]
