# Generated by Django 3.2.11 on 2022-01-19 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gtin_fields.fields
import gtin_fields.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.URLField(choices=[('https://schema.org/DamagedCondition', 'Damaged'), ('https://schema.org/NewCondition', 'New'), ('https://schema.org/RefurbishedCondition', 'Refurbished'), ('https://schema.org/UsedCondition', 'Used')])),
                ('name', models.CharField(db_index=True, max_length=256)),
                ('cell_plan_name', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('part_number', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('sku', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('ean', gtin_fields.fields.EAN13Field(blank=True, max_length=13, null=True, validators=[gtin_fields.validators._EAN13Validator()], verbose_name='EAN-13')),
                ('key', models.CharField(db_index=True, max_length=256)),
                ('url', models.URLField(db_index=True, max_length=512)),
                ('discovery_url', models.URLField(db_index=True, max_length=512)),
                ('picture_urls', models.TextField(blank=True, null=True)),
                ('description', models.TextField(null=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('last_association', models.DateTimeField(blank=True, null=True)),
                ('last_staff_access', models.DateTimeField(blank=True, null=True)),
                ('last_pricing_update', models.DateTimeField()),
                ('last_association_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('last_staff_access_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.store')),
            ],
        ),
    ]
