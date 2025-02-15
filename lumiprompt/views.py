from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import LumiPrompt
from .serializers import LumiPromptSerializer


def post(request):
    posts = LumiPrompt.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'lumiprompt/main.html',context)

# API VIEW

class PromptListAPIVIew(APIView):
    @swagger_auto_schema(
        operation_summary= "프롬프트 목록 조회,",
        operation_description= "저장된 모든 프롬프트를 조회하는 API 입니다.",
        responses={200: LumiPromptSerializer(many=True), 401:"Invalid token or token expired."}
    )
    def get(self, request):
        prompts = LumiPrompt.objects.all()
        serializer = LumiPromptSerializer(prompts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PromptDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_summary= "카드 상세 조회",
        operation_description = "id에 해당하는 프롬프트 정보를 반환합니다.",
        responses={200: LumiPromptSerializer, 404: "Not found"}

    )
    def get(self, request, id):
        prompt = get_object_or_404(LumiPrompt, id= id)
        serializer = LumiPromptSerializer(prompt)
        return Response(serializer.data, status=status.HTTP_200_OK)

