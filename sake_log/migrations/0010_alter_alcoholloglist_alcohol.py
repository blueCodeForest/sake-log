# Generated by Django 3.2.9 on 2022-01-14 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sake_log', '0009_auto_20220114_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alcoholloglist',
            name='alcohol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alcohol_log', to='sake_log.displayalcohollist'),
        ),
    ]