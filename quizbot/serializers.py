from rest_framework import serializers
from .models import User, Question, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__" # 모든 필드 직렬화


class QuestionSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() # 카테고리 이름을 문자열로 반환

    class Meta:
        model = Question
        fields = "__all__" # 모든 필드 직렬화


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"