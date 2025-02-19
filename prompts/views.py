import os
from dotenv import load_dotenv
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404,render, HttpResponse
from .utils import VectorDBManager
from lumiprompt.models import LumiPrompt
from .serializers import PromptListSerializer, PromptDetailSerializer


# api key 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

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
        


def create_db_view(request):
    """ 벡터 DB 생성 및 저장을 실행하는 뷰 함수 """
    db_manager = VectorDBManager()
    
    db_manager.load_documents()
    db_manager.split_into_chunks()  # ✅ 메서드명 수정 (기존 오류 
    db_manager.generate_embeddings()
    db_manager.create_vector_db()
    db_manager.save_vector_db()
    
    # 템플릿이 있으면 render(), 없으면 HttpResponse 반환
    if os.path.exists("templates/db_created.html"):
        return render(request, 'db_created.html')
    return HttpResponse("✅ 벡터 DB 생성 완료!")

def load_db_view(request):
    """ 벡터 DB 로드를 실행하는 뷰 함수 """
    db_manager = VectorDBManager()
    db_manager.load_vector_db()
    
    # 템플릿이 있으면 render(), 없으면 HttpResponse 반환
    if os.path.exists("templates/db_loaded.html"):
        return render(request, 'db_loaded.html')
    return HttpResponse("✅ 벡터 DB 로드 완료!")


