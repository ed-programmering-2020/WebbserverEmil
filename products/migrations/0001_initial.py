# Generated by Django 2.2.6 on 2020-05-11 09:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, null=True, verbose_name='name')),
                ('model_number', models.CharField(blank=True, max_length=128, null=True, unique=True, verbose_name='model number')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('effective_price', models.PositiveIntegerField(null=True)),
                ('active_price', models.PositiveIntegerField(null=True)),
                ('height', models.DecimalField(decimal_places=1, help_text='in millimeters', max_digits=3, null=True)),
                ('width', models.PositiveSmallIntegerField(help_text='in millimeters', null=True)),
                ('depth', models.PositiveSmallIntegerField(help_text='in millimeters', null=True)),
                ('weight', models.DecimalField(decimal_places=2, help_text='in kilograms', max_digits=3, null=True)),
                ('disclaimer', models.CharField(blank=True, max_length=128, null=True, verbose_name='disclaimer')),
                ('is_active', models.BooleanField(default=False)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('guarantee', models.DecimalField(decimal_places=1, help_text='in years', max_digits=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GraphicsCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=4, max_digits=6, null=True, verbose_name='score')),
                ('value', models.CharField(max_length=128, null=True, verbose_name='value')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=256, verbose_name='url')),
                ('placement', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=4, max_digits=6, null=True, verbose_name='score')),
                ('value', models.CharField(max_length=128, null=True, verbose_name='value')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('short_url', models.CharField(max_length=64, verbose_name='short url')),
                ('url', models.CharField(max_length=256, verbose_name='url')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MetaProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('model_number', models.CharField(max_length=128, null=True, verbose_name='model number')),
                ('availability', models.PositiveSmallIntegerField(null=True)),
                ('standard_price', models.PositiveIntegerField(null=True)),
                ('campaign_price', models.PositiveIntegerField(blank=True, null=True)),
                ('shipping', models.PositiveSmallIntegerField(null=True)),
                ('used', models.BooleanField(default=False)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('review_count', models.PositiveSmallIntegerField(null=True)),
                ('url', models.CharField(max_length=128, verbose_name='url')),
                ('is_active', models.BooleanField(default=True)),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meta_products', to='products.Website')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meta_products', to='products.BaseProduct')),
            ],
        ),
        migrations.CreateModel(
            name='ImageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256)),
                ('secondary_text', models.CharField(max_length=512)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_infos', to='products.Image')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Website'),
        ),
        migrations.AddField(
            model_name='image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.BaseProduct'),
        ),
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('baseproduct_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.BaseProduct')),
                ('screen_size', models.DecimalField(decimal_places=1, help_text='in inches', max_digits=3, null=True)),
                ('resolution', models.PositiveSmallIntegerField(help_text='in pixels', null=True)),
                ('refresh_rate', models.PositiveSmallIntegerField(help_text='in hertz', null=True)),
                ('panel_type', models.CharField(choices=[('tn', 'TN'), ('va', 'VA'), ('ips', 'IPS'), ('retina', 'Retina'), ('oled', 'OLED')], max_length=128, null=True)),
                ('storage_type', models.CharField(choices=[('hdd', 'HDD'), ('ssd', 'SSD')], max_length=128, null=True)),
                ('storage_size', models.PositiveSmallIntegerField(help_text='in gigabytes', null=True)),
                ('battery_time', models.DecimalField(blank=True, decimal_places=1, help_text='in hours', max_digits=3, null=True)),
                ('ram_capacity', models.PositiveSmallIntegerField(help_text='in gigabytes', null=True)),
                ('color', models.CharField(help_text='primary color', max_length=128, null=True)),
                ('operating_system', models.CharField(max_length=128, null=True)),
                ('graphics_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='laptops', to='products.GraphicsCard')),
                ('processor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='laptops', to='products.Processor')),
            ],
            bases=('products.baseproduct',),
        ),
    ]
