# Generated by Django 5.1 on 2025-03-08 13:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='api.loancustomer'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='loan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='api.loan'),
        ),
    ]
