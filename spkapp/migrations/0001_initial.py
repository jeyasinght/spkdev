# Generated by Django 4.1.1 on 2022-10-04 12:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='NA', max_length=40)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spkapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='order_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester', models.CharField(max_length=40)),
                ('projectname', models.CharField(choices=[('Siltronics - External Works', 'Siltronics - External Works')], max_length=30)),
                ('approver', models.CharField(max_length=40)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Approved', 'Approved')], default='Draft', max_length=10)),
                ('quantity', models.IntegerField()),
                ('remarks', models.TextField()),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_date', models.DateField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spkapp.category')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spkapp.product')),
            ],
        ),
    ]
