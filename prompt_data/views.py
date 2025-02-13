import os
import csv
from django.http import HttpResponse
from django.conf import settings  # ✅ Django 프로젝트 경로 가져오기
from django.shortcuts import render
from .models import Lumiprompt

def prompt_update(request):
    # ✅ 절대 경로를 사용하여 CSV 파일 찾기
    csv_path = os.path.join(settings.BASE_DIR, "Datas", "prompt_data.csv")

    # ✅ 파일 존재 여부 체크
    if not os.path.exists(csv_path):
        return HttpResponse(f"❌ CSV 파일이 없습니다: {csv_path}", status=400)

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 첫 번째 줄(헤더) 건너뛰기

        for row in reader:
            # 중복된 id를 건너뛰기
            if not Lumiprompt.objects.filter(id=int(row[0])).exists():
                Lumiprompt.objects.create(
                    id=int(row[0]),
                    title=row[1],
                    content=row[2],
                )

    return HttpResponse("✅ CSV 데이터가 성공적으로 업데이트되었습니다!")

def prompt_list(request):
    # Lumiprompt 모델의 모든 객체를 가져옵니다.
    prompts = Lumiprompt.objects.all()
    # 템플릿에 객체 리스트를 전달하여 렌더링합니다.
    return render(request, 'prompt_data/prompt_list.html', {'prompts': prompts})
