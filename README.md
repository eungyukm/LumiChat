# LumiChat

## 개요
본 프로젝트는 **LangChain**과 **Django**를 활용하여 **다양한 상황에서 활용할 수 있는 챗봇**을 개발하는 것입니다. 사전 정의된 프롬프트를 활용하며, 필요에 따라 **RAG (Retrieval-Augmented Generation)** 방식으로 데이터를 활용할 계획입니다.

## 주요 기능
- **다양한 도메인에 맞는 정보 제공**
  - 특정 주제에 대한 맞춤형 가이드 제공
- **문맥을 이해하는 자연어 처리 기반 응답**
  - LangChain을 활용한 대화 흐름 유지 및 문맥 이해
- **프롬프트 기반 챗봇 개발**
  - 초기 프롬프트를 표현하는 게시판 형태의 페이지 1개 제작
  - 이후 RAG를 활용한 챗봇 구축

## 기술 스택
- **백엔드**: Django, Django Rest Framework (DRF)
- **AI 모델**: OpenAI API (GPT), LangChain
- **데이터베이스**: SQLLite
- **배포 환경**: 로컬 환경에서 운영 (Docker, AWS 미사용)
- **프론트엔드**: 간단한 GPT 기반 인터페이스 (1페이지 구성)

## 설치 및 실행 방법
### 1. 환경 설정
필요한 패키지를 설치하고 환경 변수를 설정합니다.

```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # (Windows의 경우 `venv\Scripts\activate`)

# 필수 패키지 설치
pip install -r requirements.txt

# .env 파일 생성 (OpenAI API 키 포함)
cp .env.example .env
```

### 2. 데이터베이스 설정
```bash
python manage.py migrate
python manage.py createsuperuser  # 관리자 계정 생성 (옵션)
```

### 3. 서버 실행
```bash
python manage.py runserver
```

## API 명세
- `GET /api/v1/prompts/` → 모든 프롬프트 목록 조회
- `GET /api/v1/prompts/{prompt_id}/` → 특정 프롬프트 정보 조회
- `POST /api/v1/chat/` → 챗봇과의 대화 요청 (입력: 질문, 출력: 답변)

## 개발 단계
1. **1단계:** 프롬프트 게시판 형태로 구성된 페이지 1개 제작
2. **2단계:** 해당 프롬프트를 활용한 LangChain 기반 챗봇 구현
3. **3단계:** 프롬프트와 Vector DB를 연결하여 RAG 기반 챗봇 완성

## 기여 방법
1. 저장소를 포크하고 브랜치를 생성합니다.
2. 기능을 개발하고 PR을 생성합니다.
3. 코드 리뷰 후 머지합니다.

## 라이선스
본 프로젝트는 MIT 라이선스를 따릅니다.


