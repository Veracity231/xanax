# Generated by Django 2.0 on 2017-12-21 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='overdosed',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]