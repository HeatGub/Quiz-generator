# Generated by Django 4.1.7 on 2023-03-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_quiz_by_player'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='subject',
            new_name='topic',
        ),
        migrations.AddField(
            model_name='quiz',
            name='all_ok',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quiz',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
