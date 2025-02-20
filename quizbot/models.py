from django.db import models
from django.core.validators import MinValueValidator # 음수가 되지않도록

# 로그인 없이 사용자 이름만 저장, 점수 관리
class User(models.Model):
    username = models.CharField(max_length=30, unique=True) # 사용자 이름 중복 불가
    score = models.IntegerField(default=0, validators=[MinValueValidator(0)]) # 시작 점수 0

    def __str__(self):
        return f"{self.username} ({self.score}점)"


# 퀴즈 Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True) # Category 이름 중복 불가

    def __str__(self):
        return self.name


# 퀴즈 문제 저장
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # Category 연결
    text = models.TextField() # 문제 내용
    answer = models.CharField(max_length=255) # correct answer

    def save(self, *args, **kwargs):
        self.answer = self.answer.lower()  # 정답을 소문자로 변환 후 저장
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.text} - {self.answer}"

# chatbot/models.py

from django.db import models

class Conversation(models.Model):
    user_input = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation at {self.timestamp}"
