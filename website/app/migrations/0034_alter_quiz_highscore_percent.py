# Generated by Django 4.1.7 on 2023-03-17 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_alter_quiz_highscore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='highscore_percent',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4),
        ),
    ]
