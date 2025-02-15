from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from lumiprompt.models import LumiPrompt
from .serializers import PromptListSerializer, PromptDetailSerializer

class PromptsListView(APIView):

    def get(self, request, pk=None):
        if pk:  # 상세 조회
            prompt = get_object_or_404(LumiPrompt, id=pk)
            serializer = PromptDetailSerializer(prompt)
            return Response(serializer.data)

        elif 'random' in request.path:  # 랜덤 프롬포트
            try:
                prompt = get_object_or_404(LumiPrompt, pk=LumiPrompt.objects.order_by('?').first().pk)
                serializer = PromptDetailSerializer(prompt)
                return Response(serializer.data)
            except AttributeError:
                return Response({"message": "No prompts available"}, status=status.HTTP_404_NOT_FOUND)

        elif request.GET.get('search'):  # 검색
            keyword = request.GET.get('search')
            prompts = LumiPrompt.objects.filter(Q(title__icontains=keyword))
            if prompts.exists():
                serializer = PromptListSerializer(prompts, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "No prompts found"}, status=status.HTTP_404_NOT_FOUND)

        else:  # 목록 조회
            prompts = LumiPrompt.objects.all()
            serializer = PromptListSerializer(prompts, many=True)
            return Response(serializer.data)