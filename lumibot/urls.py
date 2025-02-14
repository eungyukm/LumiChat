from django.urls import path
from .views import ChatBotView  # views.py에서 ChatBotView 가져오기

urlpatterns = [
    path("", ChatBotView.as_view(), name="chatbot"),  # 기본 URL
]
