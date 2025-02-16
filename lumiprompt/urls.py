from django.urls import path
from . import views
from .views import PromptListAPIView, PromptDetailAPIView, RandomPromptAPIView, SearchPromptAPIView

app_name='lumiprompt' # App name

urlpatterns = [
    path("", PromptListAPIView.as_view(), name="prompt-list"),  # ✅ URL을 ""로 변경
    path("<int:id>/", PromptDetailAPIView.as_view(), name="prompt-detail"),
    path("random/", RandomPromptAPIView.as_view(), name="random-prompt"),
    path("search/", SearchPromptAPIView.as_view(), name="search-prompt"),
]