# Generated by Django 4.1.7 on 2023-03-14 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_question_correct'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Choice',
            new_name='Answer',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='choice_text',
            new_name='answer_text',
        ),
    ]
