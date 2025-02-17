from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from lumiprompt.models import LumiPrompt
from .serializers import PromptListSerializer, PromptDetailSerializer

class PromptsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LumiPrompt.objects.all()
    serializer_class = PromptListSerializer

    # 상세 조회
    def retrieve(self, request, pk=None):
        prompt = get_object_or_404(LumiPrompt, id=pk)
        serializer = PromptDetailSerializer(prompt)
        return Response(serializer.data)

    # 검색 기능
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        keyword = request.GET.get('search', None)
        if keyword:
            prompts = LumiPrompt.objects.filter(Q(title__icontains=keyword))
            if prompts.exists():
                serializer = PromptDetailSerializer(prompts, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "No prompts found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "No keyword provided"}, status=status.HTTP_400_BAD_REQUEST)

    # 랜덤 프롬프트 기능
    @action(detail=False, methods=['get'], url_path='random')
    def random(self, request):
        try:
            prompt = get_object_or_404(LumiPrompt, pk=LumiPrompt.objects.order_by('?').first().pk)
            serializer = PromptListSerializer(prompt)
            return Response(serializer.data)
        except AttributeError:
            return Response({"message": "No prompts available"}, status=status.HTTP_404_NOT_FOUND)
