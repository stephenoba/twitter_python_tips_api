# Generated by Django 3.2 on 2021-06-21 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('python_tips', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tip',
            options={'ordering': ['timestamp'], 'verbose_name': 'Tip', 'verbose_name_plural': 'Tips'},
        ),
    ]
