from django.db import models

# 로그인 없이 사용자 이름만 저장, 점수 관리
class User(models.Model):
    username = models.CharField(max_length=30, unique=True) # 사용자 이름 중복 불가
    score = models.IntegerField(default=0) # 시작 점수 0

    def __str__(self):
        return f"{self.username} ({self.score}점"


# 퀴즈 Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True) # Category 이름 중복 불가

    def __str__(self):
        return self.name


# 퀴즈 문제 저장
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Category 연결
    text = models.TextField() # 문제 내용
    answer = models.CharField(max_length=255) # correct answer

    def __str__(self):
        return f"{self.text} - {self.answer}"