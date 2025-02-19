from django.urls import path

from quizbot.views import (
    QuizStartView, QuizCategoryView, SubmitAnswerView,
    QuizQuestionView, QuizScoreView, QuizRankVIew
)


app_name = "quiz"


urlpatterns = [
    path("api/v1/quiz/", QuizStartView.as_view(), name="quiz-start"),
    path("api/v1/quiz/category/", QuizCategoryView.as_view(), name="quiz-category"),
    path("api/v1/quiz/answer/", SubmitAnswerView.as_view(), name="quiz-answer"),
    path("api/v1/quiz/random/", QuizQuestionView.as_view(), name="quiz-random"),
    path("api/v1/quiz/score/", QuizScoreView.as_view(), name="quiz-score"),
    path("api/v1/quiz/rank/", QuizRankVIew.as_view(), name="quiz-rank"),
]