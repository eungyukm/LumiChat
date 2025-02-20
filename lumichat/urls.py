"""
URL configuration for lumichat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from lumiprompt.views import HomeView

schema_view = get_schema_view(
    openapi.Info(
        title="ChatBot API",
        default_version="v1",
        description="챗봇 API 문서",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
"""
urlpatterns = [
    path("admin/", admin.site.urls),
    # lumiprompt
    path('prompt/', include('lumiprompt.urls')),
    # prompt_data
    path("prompt_data/", include('prompt_data.urls')),
    # prompts
    path('GET /api/v1/prompts/',include('prompts.urls')),
    # lumibot
    path("api/v1/chat/", include("lumibot.urls")),
    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),# type: ignore
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),# type: ignore
    path("swagger.json/", schema_view.without_ui(cache_timeout=0)),# type: ignore
]
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),

    # lumiprompt
    path("api/v1/lumiprompts/", include("lumiprompt.urls")),
    
    # prompts
    path('api/v1/prompts/', include('prompts.urls')),
    # path('api/v1/vector_db/', include('prompts.urls')),


    # lumibot (챗봇 관련 API)
    path("api/v1/chat/", include("lumibot.urls")),

    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),#type:ignore
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),#type:ignore
    path("swagger.json/", schema_view.without_ui(cache_timeout=0)),#type:ignore

    # 퀴즈 챗봇 API
    path("api/v1/quizbot/", include("quizbot.urls")),
]
