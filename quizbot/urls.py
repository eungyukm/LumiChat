from django.urls import path
from quizbot.views import QuizBotView

app_name = "quiz"

urlpatterns = [
    path("quizbot/", QuizBotView.as_view(), name="quizbot"),
]
