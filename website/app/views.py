from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Answer, BetweenAllUpdates
from .forms import FormClass
from django.shortcuts import redirect
from django.views.generic.list import ListView
# from app.callGPT import JSONresponse
from app.callGPT import callGPT
from django.http import HttpResponse
import datetime

def home_view(request):
    return render(request, "home.html")

def form_view(request):
    try:
        if request.POST: 
            form = FormClass(request.POST)
            #print(type(form))
            temperature = int(form['temper'].value())/100
            # print("temperature: " + str(temperature))
            if form.is_valid():
                gpt_out = callGPT(form['topic'].value(), form['nquestions'].value(), form['nanswers'].value(), temperature)
                # print(gpt_out)
                quiz = Quiz(
                    topic = form['topic'].value(),
                    timer = form['timer'].value(), 
                    questions_form = form['nquestions'].value(), 
                    answers_form = form['nanswers'].value(), 
                    finish_reason = gpt_out['finishReason'], 
                    temper=form['temper'].value(),
                    questions_amount = gpt_out['questionsAmount'], 
                    answers_mode = gpt_out['answersMode'], 
                    answers_sublists_equal = gpt_out['answersSublistsEqual'], 
                    corrects_valid_range = gpt_out['correctsValidRange'],
                    response_text = gpt_out['responseText'],
                    visible = gpt_out['visible'],
                    all_ok = gpt_out['allOk']
                    )
                quiz.save()
                for i in range (len(gpt_out['questions'])):
                    question = Question(quiz=quiz, question_text=gpt_out['questions'][i], correct=gpt_out['corrects'][i])
                    question.save()
                    for j in range (len(gpt_out['answers'][i])):
                        answer = Answer(question = question, answer_text = gpt_out['answers'][i][j])
                        answer.save()
                # print("Saved set's id: " + str(quiz.pk))
                if quiz.visible == True:
                    return redirect(quiz.get_absolute_url()) #method from models, necessary for this redirect game/id
                else:
                    return render(request, "generate_error.html", {'form' : FormClass})
        return render(request, "generate.html", {'form' : FormClass})
    except: #when response dictionary is not valid
        return render(request, "generate_error.html", {'form' : FormClass})

def generate_error_view(request):
    return render(request, "generate_error.html")

def game_view(request, set_id):
    quiz = get_object_or_404(Quiz, pk=set_id)
    quiz.views_counter = quiz.views_counter +1
    quiz.save()
    if quiz.visible == True: #render only visible quizes
        timer = quiz.timer
        nq = quiz.questions_amount
        na = quiz.answers_mode
        questionsQuery = quiz.question_set.all()
        questions = []
        answers = []
        corrects = []
        for question in questionsQuery:
            questions.append(str(question))
            corrects.append(str(question.correct))
            answersQuery = question.answer_set.all().values_list('answer_text', flat=True)
            answersAppend = []
            for answer in answersQuery:
                answersAppend.append(str(answer))
            answers.append(answersAppend)
        return render(request, 'game.html', {'quizID': set_id, 'questions':questions, 'answers':answers, 'corrects':corrects, 'timer': timer, 'nq':nq, 'na':na})
    else:
        return render(request, "404.html", status = 404)

def pass_high_view(request, set_id):
    selected = get_object_or_404(Quiz, pk=set_id)
    highscore = selected.highscore
    return HttpResponse(highscore)

def save_view(request):
    if request.method == "POST":
        # print(request)
        forID =  request.POST['forID']
        quiz = Quiz.objects.get(pk=forID)
        quiz.highscore = request.POST['score_points']
        quiz.highscore_percent = request.POST['score_percent']
        quiz.by_player = request.POST['nickname']
        if quiz.last_update_date: #if there was none or smth
            between_last_updates = datetime.datetime.now() - quiz.last_update_date
            quiz.last_update_date = datetime.datetime.now()
            quiz.between_last_updates = between_last_updates
            between_updates = BetweenAllUpdates(quiz=quiz, between_updates = between_last_updates, highscore_percent_updated = request.POST['score_percent'], by_player_updated = request.POST['nickname'])
            Quiz.full_clean(quiz) #  raise ValidationError(errors) django.core.exceptions.ValidationError: {'by_player': ['Ensure this value has at most 20 characters (it has 32).']}
            between_updates.save()
            quiz.save()
        else:
            quiz.last_update_date = datetime.datetime.now()
            between_last_updates = datetime.datetime.now() - quiz.created
            quiz.between_last_updates = between_last_updates
            between_updates = BetweenAllUpdates(quiz=quiz, between_updates = between_last_updates, highscore_percent_updated = request.POST['score_percent'], by_player_updated = request.POST['nickname'])
            Quiz.full_clean(quiz) #  raise ValidationError(errors) django.core.exceptions.ValidationError: {'by_player': ['Ensure this value has at most 20 characters (it has 32).']}
            between_updates.save()
            quiz.save()
        return redirect('home') #redirecting from /save_high url

class QuizListView(ListView): #highscores
    model = Quiz
    # queryset = Quiz.objects.all()
    # queryset = Quiz.objects.filter(visible=True)
    queryset= Quiz.objects.filter(visible=True).order_by('-highscore') #Deployment queryset
    paginate_by = 20
    template_name = "highscores.html"

def handler400(request, exception):
    return render(request, "400.html", status = 400)

def handler403(request, exception):
    return render(request, "403.html", status = 403)

def handler404(request, exception):
    return render(request, "404.html", status = 404)

def handler408(request, exception):
    return render(request, "408.html", status = 408)

def handler500(request):
    return render(request, "500.html", status = 500)

def handler504(request):
    return render(request, "504.html", status = 504)