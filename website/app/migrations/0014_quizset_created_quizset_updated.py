# Generated by Django 4.1.7 on 2023-03-07 21:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_quizset_highscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizset',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 7, 21, 52, 8, 848315)),
        ),
        migrations.AddField(
            model_name='quizset',
            name='updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 7, 21, 52, 8, 848330)),
        ),
    ]
