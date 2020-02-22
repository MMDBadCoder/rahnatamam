# Generated by Django 3.0.3 on 2020-02-20 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0009_auto_20200218_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('ACTIVATE', 'Activate')], max_length=30)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Account')),
            ],
        ),
    ]