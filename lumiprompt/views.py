import random

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import LumiPrompt
from .serializers import LumiPromptSerializer


class HomeView(TemplateView):
    template_name = "lumiprompt/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 기존 context 가져 오기
        context["posts"] = LumiPrompt.objects.all()
        return context


# API VIEW

class PromptListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="프롬프트 목록 조회",
        operation_description="저장된 모든 프롬프트를 조회하는 API 입니다.",
        responses={
            200: LumiPromptSerializer(many=True),
            401: openapi.Response(description="Invalid token or token expired.")
        }
    )
    def get(self, request):
        prompts = LumiPrompt.objects.all()
        serializer = LumiPromptSerializer(prompts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PromptDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="카드 상세 조회",
        operation_description="id에 해당하는 프롬프트 정보를 반환합니다.",
        responses={
            200: LumiPromptSerializer(many=False),
            404: openapi.Response(description="Not found")
        }
    )
    def get(self, request, id):
        prompt = get_object_or_404(LumiPrompt, id=id)
        serializer = LumiPromptSerializer(prompt)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RandomPromptAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="랜덤 프롬프트 조회",
        operation_description="랜덤으로 프롬프트를 반환합니다.",
        responses={
            200: LumiPromptSerializer(many=False),
            404: openapi.Response(description="No prompts available")
        }
    )
    def get(self, request):
        queryset = LumiPrompt.objects.all()

        if not queryset.exists():
            return Response(
                {"detail": "No prompts available"},
                status=status.HTTP_404_NOT_FOUND
            )

        prompt = random.choice(list(queryset))
        serializer = LumiPromptSerializer(prompt)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchPromptAPIView(APIView):
    @swagger_auto_schema(
        operation_summary= "프롬프트 검색",
        operation_description= "키워드(q)를 포함하는 프롬프트 목록을 반환합니다.",
        manual_parameters=[
            openapi.Parameter(
                "q", openapi.IN_QUERY,
                description="검색 키워드",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: LumiPromptSerializer(many=True),
            400: openapi.Response(description="Bad request")
        }
    )
    def get(self, request):
        query = request.GET.get("q", "").strip()
        if not query:
            return Response(
                {"detail": "검색어를 입력하세요"},
                status=status.HTTP_400_BAD_REQUEST
            )

        prompts = LumiPrompt.objects.filter(
            Q(title__icontains=query) | Q(prompt__icontains=query)
        )

        serializer = LumiPromptSerializer(prompts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

