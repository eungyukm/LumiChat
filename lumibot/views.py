from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ChatBotView(APIView):
    """
    LangChain 기반 챗봇 API
    사용자가 질문과 추가 정보를 입력하면 응답을 생성하여 반환
    """

    @swagger_auto_schema(
        operation_description="챗봇에게 질문을 보내고 응답을 받습니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "question": openapi.Schema(type=openapi.TYPE_STRING, description="질문 내용", example="버서커 클래스 특징 알려줘"),
                "language": openapi.Schema(type=openapi.TYPE_STRING, description="응답 언어 (예: 'ko', 'en')", example="ko"),
                "mode": openapi.Schema(type=openapi.TYPE_STRING, description="챗봇 응답 모드 (예: 'detailed', 'simple')", example="detailed"),
            },
            required=["question"],  # 필수 파라미터 설정
        ),
        responses={200: openapi.Response("챗봇 응답", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "question": openapi.Schema(type=openapi.TYPE_STRING, description="사용자가 입력한 질문"),
                "language": openapi.Schema(type=openapi.TYPE_STRING, description="응답 언어"),
                "mode": openapi.Schema(type=openapi.TYPE_STRING, description="응답 모드"),
                "answer": openapi.Schema(type=openapi.TYPE_STRING, description="챗봇의 응답"),
            },
        ))},
    )
    def post(self, request):
        """챗봇에게 질문을 보내고 응답을 받음 (파라미터 포함)"""
        question = request.data.get("question", "")
        language = request.data.get("language", "ko")  # 기본값: 한국어
        mode = request.data.get("mode", "simple")  # 기본값: 간단한 답변

        if not question:
            return Response({"error": "질문을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 응답 생성 (현재는 단순 응답, 실제 LangChain 호출 가능)
        answer = f"[{language.upper()} | {mode.capitalize()}] {question}에 대한 응답입니다."

        return Response({
            "question": question,
            "language": language,
            "mode": mode,
            "answer": answer
        }, status=status.HTTP_200_OK)
