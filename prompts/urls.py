from django.urls import path
from .views import PromptsListView

urlpatterns = [
    path('', PromptsListView.as_view()),             # 목록 조회 & 검색
    path('<int:pk>/', PromptsListView.as_view()),    # 상세 조회
    path('random/', PromptsListView.as_view()),      # 랜덤 프롬프트 조회
]
