# Generated by Django 3.2 on 2021-06-22 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_tips', '0003_alter_tip_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tip',
            name='tweet_id',
            field=models.IntegerField(db_index=True, unique=True, verbose_name='Tweet ID'),
        ),
    ]
