from django.urls import path
from quizzes import views

urlpatterns = [
    path('session/', views.SessionView.as_view()),
    path('question/', views.SimpleQuestionView.as_view()),
]