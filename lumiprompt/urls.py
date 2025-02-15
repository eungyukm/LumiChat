from django.urls import path
from . import views
from .views import PromptListAPIVIew, PromptDetailAPIView

app_name='lumiprompt' # App name
urlpatterns=[
    path('', views.post, name='post'), # Path for the prompt view

    path("api/v1/prompts/", PromptListAPIVIew.as_view()),
    path("api/v1/<int:id>/", PromptDetailAPIView.as_view()),
]