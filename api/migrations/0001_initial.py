# Generated by Django 3.2.11 on 2022-01-16 18:09

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('iso_code', models.CharField(max_length=2)),
                ('flag', sorl.thumbnail.fields.ImageField(upload_to='country_flags')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('storescraper_class', models.CharField(db_index=True, max_length=255, null=True)),
                ('storescraper_extra_args', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', sorl.thumbnail.fields.ImageField(default='default.jpg', upload_to='store_logos')),
            ],
        ),
        migrations.CreateModel(
            name='StoreType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
