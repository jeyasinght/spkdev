# Generated by Django 4.1.1 on 2022-11-21 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spkapp', '0006_vendor_order_model_orderno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_model',
            name='vendor',
            field=models.ForeignKey(blank=True, default='None', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spkapp.vendor'),
        ),
    ]
