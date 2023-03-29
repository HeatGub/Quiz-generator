# Generated by Django 4.1.7 on 2023-03-14 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_rename_choice_answer_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='QuizSet',
        ),
        migrations.RenameField(
            model_name='quiz',
            old_name='byplayer',
            new_name='by_player',
        ),
        migrations.AddField(
            model_name='quiz',
            name='answers_form',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='errors',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='quiz',
            name='finish_reason',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='quiz',
            name='highscore_percent',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='qestions_form',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='timer',
            field=models.PositiveSmallIntegerField(default=10),
        ),
    ]
