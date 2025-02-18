from lumiprompt.models import LumiPrompt
from rest_framework import serializers

class PromptDetailSerializer(serializers.ModelSerializer): # 디테일 시리얼라이저저
    class Meta:
        model = LumiPrompt
        fields = ('id', 'title', 'prompt')

class PromptListSerializer(serializers.ModelSerializer): # 일반 리스트 시리얼라이저
    class Meta:
        model = LumiPrompt
        fields = ('title',)