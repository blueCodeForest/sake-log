# Generated by Django 3.2.9 on 2022-01-07 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sake_log', '0005_alter_drankalcohollist_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drankalcohollist',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
