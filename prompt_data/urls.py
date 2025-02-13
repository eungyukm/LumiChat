from django.urls import path
from . import views

urlpatterns = [
    path('', views.prompt_update, name="data"),
    path('list/', views.prompt_list, name="prompt_list"),
]