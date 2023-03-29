from django import forms
from django.forms import ModelForm
from .models import Quiz

class FormClass(ModelForm):
    #topic = forms.CharField(max_length = 20, label='Quiz Topic', widget= forms.TextInput(attrs={'placeholder':'Enter your first name'})) #placeholder messes validation
    topic = forms.CharField(max_length = 20, label='Topic')
    nquestions = forms.IntegerField(min_value = 1, max_value = 20, label='Questions (1-20)')
    nanswers = forms.IntegerField(min_value = 2, max_value = 10, label='Answers to a question (2-10)')
    temper = forms.IntegerField(min_value = 0, max_value = 100, label='GPT temper (0-100)')
    timer = forms.IntegerField(min_value = 1, max_value = 99, label='Time limit for a question (1-99s)')
    class Meta:
        model = Quiz
        fields = ['topic', 'nquestions', 'nanswers', 'temper', 'timer']