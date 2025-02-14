from django.db import models

# 챗봇 질문 및 응답 저장 모델
class ChatMessage(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)