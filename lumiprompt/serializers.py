from rest_framework import serializers
from lumiprompt.models import LumiPrompt

class LumiPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumiPrompt
        fields = ["id", "title", "prompt"]