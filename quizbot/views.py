import openai
import json
import os
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class QuizBotView(APIView):
    @swagger_auto_schema(
        operation_summary="퀴즈 챗봇",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'action': openapi.Schema(type=openapi.TYPE_STRING, description="요청 기능 (start, quiz, answer)", example="quiz"),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="사용자 이름", example="test_user"),
                'difficulty': openapi.Schema(type=openapi.TYPE_STRING, description="퀴즈 난이도", example="medium"),
                'answer': openapi.Schema(type=openapi.TYPE_STRING, description="사용자 답변", example="B"),
                'quiz_id': openapi.Schema(type=openapi.TYPE_STRING, description="퀴즈 ID", example="123e4567-e89b-12d3-a456-426614174000"),
            },
            required=['action']
        ),
        responses={200: "요청 성공", 400: "잘못된 요청"}
    )
    def post(self, request):
        action = request.data.get("action", "").strip().lower()

        if action == "start":
            username = request.data.get("username", "").strip()
            if not username:
                return Response({"error": "사용자 이름을 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
            cache.set(f"quiz_user_{request.session.session_key}", username, timeout=3600)
            return Response({"message": f"{username}님, 퀴즈를 시작합니다!"}, status=status.HTTP_200_OK)



        elif action == "quiz":
            difficulty = request.data.get("difficulty", "medium")
            prompt = f"""

                {difficulty} 난이도의 개발 관련 객관식 퀴즈를 JSON 형식으로 생성하세요.

                {{
                    "question": "문제 내용",
                    "choices": {{"A": "선택지1", "B": "선택지2", "C": "선택지3", "D": "선택지4"}},
                    "answer": "정답",
                    "explanation": "해설"
                }}
            """

            try:
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": prompt}],
                    max_tokens=300
                )

                quiz_json = json.loads(response.choices[0].message.content.strip())
                quiz_id = str(uuid.uuid4())
                cache.set(f"quiz_{quiz_id}", quiz_json, timeout=3600)  # 정답과 해설 포함하여 저장

                quiz_display = quiz_json.copy()
                quiz_display.pop("answer", None)  # 정답 제거
                quiz_display.pop("explanation", None)  # 해설 제거

                return Response({"message": "퀴즈가 시작됩니다!", "quiz_id": quiz_id, "quiz": quiz_display},
                                status=status.HTTP_200_OK
                                )

            except Exception as e:
                return Response({"error": f"오류 발생: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


