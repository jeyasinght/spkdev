# Generated by Django 4.1.1 on 2022-11-11 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spkapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.AlterField(
            model_name='order_model',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order_model',
            name='status',
            field=models.CharField(choices=[('Requested', 'Requested'), ('Checked', 'Checked'), ('Approved', 'Approved')], default='Requested', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AddField(
            model_name='order_model',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spkapp.units'),
        ),
        migrations.AlterField(
            model_name='order_model',
            name='projectname',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spkapp.projects'),
        ),
    ]
