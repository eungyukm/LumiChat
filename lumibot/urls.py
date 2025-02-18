from django.urls import path
from .views import LostArkChatBotView

urlpatterns = [
    path("loast_ark/", LostArkChatBotView.as_view(), name="chatbot_response"),
]
