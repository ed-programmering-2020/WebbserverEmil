# Generated by Django 2.2.6 on 2020-05-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseproduct',
            name='guarantee',
            field=models.DecimalField(decimal_places=1, help_text='in years', max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='panel_type',
            field=models.CharField(choices=[('tn', 'TN'), ('va', 'VA'), ('ips', 'IPS'), ('retina', 'Retina'), ('oled', 'OLED')], max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='storage_type',
            field=models.CharField(choices=[('hdd', 'HDD'), ('ssd', 'SSD')], max_length=128, null=True),
        ),
    ]
