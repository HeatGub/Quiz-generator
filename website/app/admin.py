from django.contrib import admin
# Register your models here.
from .models import Quiz, Question, Answer, BetweenAllUpdates
import nested_admin

class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    extra = 1

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]

class BetweenAllUpdatesInline(nested_admin.NestedStackedInline):
    model = BetweenAllUpdates
    extra = 1

class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline, BetweenAllUpdatesInline]
    search_fields = ['topic', 'by_player']
    list_display = ('id', 'views_counter', 'last_view', 'created', 'last_update_date', 'between_last_updates', 'visible', 'all_ok', 'questions_amount', 'answers_mode', 'highscore_percent', 'by_player', 'topic')
    list_filter = ['created', 'last_update_date', 'last_view', 'finish_reason', 'visible', 'all_ok']

admin.site.register(Quiz, QuizAdmin)

class BetweenAllUpdatesAdmin(nested_admin.NestedModelAdmin):
    # search_fields = ['topic', 'by_player']
    search_fields = ['by_player_updated']
    list_display = ('quiz', 'between_updates', 'highscore_percent_updated', 'by_player_updated')

admin.site.register(BetweenAllUpdates, BetweenAllUpdatesAdmin)