# Generated by Django 4.1.7 on 2023-03-19 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_quiz_between_updates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='between_updates',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
