# Generated by Django 5.2.1 on 2025-06-02 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newspaper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('in_active', 'Inactive')], default='active', max_length=20),
        ),
    ]
