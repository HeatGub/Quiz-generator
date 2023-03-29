from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse

class Quiz(models.Model):
    topic = models.CharField(max_length = 20, default = '')
    temper = models.PositiveSmallIntegerField(default = 0)
    timer = models.PositiveSmallIntegerField(default = 10)
    #highscore = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    highscore = models.PositiveSmallIntegerField(default = 0)
    highscore_percent = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    by_player = models.CharField(max_length = 20, default = '', blank=True) #validators=[RegexValidator('[+-/%<>&]', inverse_match=True)]
    questions_form = models.PositiveSmallIntegerField(default = 0)
    answers_form = models.PositiveSmallIntegerField(default = 0)
    created = models.DateTimeField(auto_now_add=True)
    last_view = models.DateTimeField(auto_now=True) #after every page visit since it saves views counter
    last_update_date = models.DateTimeField(blank = True, null=True) #saved only with highscore
    between_last_updates = models.DurationField(blank = True, null=True)
    views_counter = models.PositiveIntegerField(default = 0)
    #my 'validation' values
    finish_reason =  models.CharField(max_length=100, default = '')
    questions_amount = models.PositiveSmallIntegerField(default = 0)
    answers_mode = models.PositiveSmallIntegerField(default = 0)
    answers_sublists_equal = models.BooleanField(default = False)
    corrects_valid_range = models.BooleanField(default = False)
    visible = models.BooleanField(default = False)
    all_ok = models.BooleanField(default = False)
    response_text = models.TextField(blank = True)

    def get_absolute_url(self):
        return reverse("game", kwargs={"set_id": self.id}) #REVERSE to redirect from form
    
    def __str__(self):
        return self.topic

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    correct = models.PositiveSmallIntegerField(default = 0)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.answer_text
    
class BetweenAllUpdates(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    between_updates = models.DurationField(blank = True, null=True)
    highscore_percent_updated = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    by_player_updated = models.CharField(max_length = 20, default = '', blank=True)