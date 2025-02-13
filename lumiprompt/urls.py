from django.urls import path
from . import views

app_name='lumiprompt' # App name
urlpatterns=[
    path('', views.post, name='post'), # Path for the prompt view
]