# Generated by Django 3.0.8 on 2020-08-26 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0008_auto_20200826_2221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='details',
            old_name='phone_no',
            new_name='ph_no',
        ),
    ]