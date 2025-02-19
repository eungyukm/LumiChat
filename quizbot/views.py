from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    UserSerializer, QuestionSerializer
)




# 이름 입력 후 카테고리 목록
class QuizStartView(APIView):
    @swagger_auto_schema(
        operation_summary="이름 입력 후 퀴즈 시작",
        operation_description="사용자가 이름을 입력하면 퀴즈를 시작합니다.",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username"],
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="사용자 이름"),
        }
    ),
        responses={
            200: UserSerializer(),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        username = request.data.get("username", "")
        return Response({"message":f"{username}님 퀴즈가 시작됩니다!"}, status=status.HTTP_200_OK)


# 퀴즈 카테고리 선택 후 퀴즈 시작
class QuizCategoryView(APIView):
    @swagger_auto_schema(
        operation_summary="카테고리 선택",
        operation_description="사용자가 카테고리를 선택하면 퀴즈 시작",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["category"],
            properties={
                "category": openapi.Schema(type=openapi.TYPE_STRING, description="선택한 퀴즈 카테고리")
            },
        ),
        responses={
            200: QuestionSerializer(many=True),
            400: openapi.Response(description="Bad request")
        }

    )
    def post(self, request):
        category = request.data.get("category", "")
        return Response({"message": f"{category}을/를 풀어봅시다 !"}, status=status.HTTP_200_OK)

# 랜덤 문제 출제
class QuizQuestionView(APIView):
    @swagger_auto_schema(
        operation_summary="랜덤 문제 출제",
        operation_description="선택한 카테고리에서 랜덤 문제 출제",
        responses={
            200: QuestionSerializer()
        }
    )
    def get(self, request):
        question = {
            "question":"drf-yasg에서 Swagger 문서를 보기 위해 URL 패턴에 추가해야 하는 함수는?",
            "choices":["swagger_view()",  "get_swagger_view()",  "schema_view()", "generate_swagger_url()"]
        }
        return Response(question, status=status.HTTP_200_OK)

# 현재 점수 조회
class QuizScoreView(APIView):
    @swagger_auto_schema(
        operation_summary="현재 점수 조회",
        operation_description="현재 사용자의 총점 조회",
        responses={
            200: openapi.Response(
                description="현재 점수",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "score": openapi.Schema(type=openapi.TYPE_INTEGER, description="현재 사용자의 총점")
                    }
                )
            ),
            400: openapi.Response(description="Bad request")
        }

    )
    def get(self, request):
        return Response({"score":10}, status=status.HTTP_200_OK)


# 전체 사용자 랭킹 조회
class QuizRankVIew(APIView):
    @swagger_auto_schema(
        operation_summary="전체 사용자 순위 조회",
        operation_description="전체 사용자 순위 조회",
        responses={200: "사용자 순위"}
    )
    def get(self, request):
        ranking = [{"username":"ouxrlo", "score": 100}, {"username":"LEE", "score":40}]
        return Response({"ranking":ranking}, status=status.HTTP_200_OK)


# 정답 제출 및 채점
class SubmitAnswerView(APIView):
    @swagger_auto_schema(
        operation_summary="정답 제출 및 채점",
        operation_description="사용자가 정답 제출 및 채점",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["question_id", "answer"],
            properties={
                "question_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="문제 ID"),
                "answer": openapi.Schema(type=openapi.TYPE_STRING, description="사용자가 선택한 답"),
            },
        ),
        responses={
            200: openapi.Response(
                description="정답 제출 결과",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="정답 여부 메시지"),
                        "correct": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="정답 여부"),
                        "score": openapi.Schema(type=openapi.TYPE_INTEGER, description="현재 총점")
                    }
                )
            ),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        return Response({"message": "정답 확인 완료!"}, status=status.HTTP_200_OK)




