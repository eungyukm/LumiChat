
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .utils import VectorDBManager  # 벡터 DB 관리 클래스 불러오기

# 관광지 검색 API
class SearchLocationView(APIView):
    @swagger_auto_schema(
        operation_summary="관광지 검색",
        operation_description="관광지명이나 키워드를 입력받아 관련 정보를 반환합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["query"],
            properties={
                "query": openapi.Schema(type=openapi.TYPE_STRING, description="검색어 (관광지명 또는 키워드)")
            },
        ),
        responses={
            200: openapi.Response(
                description="검색 결과",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_STRING, description="관광지 ID"),
                            "name": openapi.Schema(type=openapi.TYPE_STRING, description="관광지명"),
                            "description": openapi.Schema(type=openapi.TYPE_STRING, description="설명"),
                        }
                    )
                )
            ),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        db_manager = VectorDBManager()

        db_manager.load_vector_db()
        
        results = db_manager.search_similar_locations(query, k=5)
        
        response_data = [
            {"id": idx, "name": doc["name"], "description": doc["description"]}
            for idx, doc in enumerate(results)
        ]
        
        return Response(response_data, status=status.HTTP_200_OK)


# 특정 관광지 상세 정보 API
class LocationDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="관광지 상세 정보",
        operation_description="특정 관광지의 ID를 입력받아 상세 정보를 반환합니다.",
        responses={
            200: openapi.Response(
                description="관광지 상세 정보",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING, description="관광지 ID"),
                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="관광지명"),
                        "description": openapi.Schema(type=openapi.TYPE_STRING, description="설명"),
                        "location": openapi.Schema(type=openapi.TYPE_STRING, description="위치 정보"),
                    }
                )
            ),
            400: openapi.Response(description="Bad request"),
            404: openapi.Response(description="Not found")
        }
    )
    def get(self, request, id):
        db_manager = VectorDBManager()
        db_manager.load_vector_db()
        
        result = db_manager.get_location_by_id(id)
        if not result:
            return Response({"error": "해당 ID의 관광지를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            "id": id,
            "name": result["name"],
            "description": result["description"],
            "location": result.get("location", "정보 없음")
        }
        return Response(response_data, status=status.HTTP_200_OK)

