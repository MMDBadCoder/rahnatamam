# Generated by Django 3.0.3 on 2020-02-18 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_auto_20200218_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='spouse',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='spouse', to='accounting.Human'),
        ),
    ]