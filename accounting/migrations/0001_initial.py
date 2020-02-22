# Generated by Django 3.0.3 on 2020-02-16 23:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('father_name', models.CharField(max_length=100)),
                ('national_id', models.CharField(max_length=10)),
                ('born_date', models.DateField()),
                ('gender', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participated_count', models.IntegerField(default=0)),
                ('entry_year', models.IntegerField(default=98)),
                ('grade', models.CharField(max_length=20)),
                ('educational_status', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=12)),
                ('college', models.CharField(max_length=20)),
                ('human', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='account', to='accounting.Human')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]