# Generated by Django 4.1.7 on 2023-03-15 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_quiz_highscore_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='temperature',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='highscore',
            field=models.FloatField(default=0),
        ),
    ]