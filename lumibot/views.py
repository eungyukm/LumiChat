from django.apps import apps
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
                "question": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="질문 내용",
                    example="로스트아크 클래스 알려줘"
                ),
                "language": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="응답 언어 (예: 'ko', 'en')",
                    example="ko"
                ),
                "mode": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="챗봇 응답 모드 (예: 'detailed', 'simple')",
                    example="detailed"
                ),
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
        """챗봇에게 질문을 보내고 응답을 받음 (LangChain 사용)"""
        question = request.data.get("question", "").strip()
        language = request.data.get("language", "ko")
        mode = request.data.get("mode", "simple")

        if not question:
            return Response({"error": "질문을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # LumibotConfig에서 LangChain 검색 체인 가져오기
        app_config = apps.get_app_config("lumibot")
        qa_chain = getattr(app_config, "qa_chain", None)

        if not qa_chain:
            return Response(
                {"error": "⚠️ 데이터베이스가 없습니다. 먼저 데이터를 불러오세요."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # LangChain을 통해 응답 생성
        response = qa_chain.invoke({"question": question})

        return Response({
            "question": question,
            "language": language,
            "mode": mode,
            "answer": response["answer"]
        }, status=status.HTTP_200_OK)
