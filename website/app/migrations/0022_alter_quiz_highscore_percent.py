# Generated by Django 4.1.7 on 2023-03-15 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_rename_qestions_form_quiz_questions_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='highscore_percent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]