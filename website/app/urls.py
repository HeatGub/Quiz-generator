from django.contrib import admin
from django.urls import path, include
from .views import home_view, game_view, form_view, generate_error_view, QuizListView, save_view, pass_high_view

handler400 = 'app.views.handler400'
handler403 = 'app.views.handler403'
handler404 = 'app.views.handler404'
handler408 = 'app.views.handler408'
handler500 = 'app.views.handler500'
handler504 = 'app.views.handler504'

urlpatterns = [
    path('', home_view, name = 'home'),
    path('generate', form_view, name = 'generate'),
    path('generate_error', generate_error_view, name = 'generate_error'),
    path('game/<int:set_id>', game_view, name = 'game'),
    path('highscores', QuizListView.as_view(), name = 'high'),
    path('save_high', save_view, name = 'save_high'),
    path('pass_high/<int:set_id>', pass_high_view, name='passhigh'),
    path('nested_admin/', include('nested_admin.urls'), name='nested_admin'),
]