# Generated by Django 4.1.7 on 2023-03-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_alter_quiz_response_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='finish_reason',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='response_text',
            field=models.TextField(blank=True),
        ),
    ]
