# Generated by Django 4.1.1 on 2022-11-11 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spkapp', '0002_projects_units_alter_order_model_remarks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='name',
            field=models.CharField(default='Siltronics - External Works', max_length=40),
        ),
    ]
