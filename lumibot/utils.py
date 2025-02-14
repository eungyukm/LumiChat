import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("⚠️ OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# LLM 설정 (GPT-4)
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, openai_api_key=openai_api_key)

# 대화 메모리
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 나무위키에서 클래스 정보를 가져오는 함수
def fetch_lostark_classes():
    url = "https://namu.wiki/w/%EB%A1%9C%EC%8A%A4%ED%8A%B8%EC%95%84%ED%81%AC/%ED%81%B4%EB%9E%98%EC%8A%A4"
    headers = {"User-Agent": "Mozilla/5.0"}  # 웹사이트 차단 방지
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ 요청 실패: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    # 본문 가져오기 (나무위키 특성상 class 기반으로 요소를 찾기 어려울 수 있음)
    content = soup.get_text(separator="\n", strip=True)
    
    return content

# 벡터DB에 저장하는 함수
def load_vector_db():
    print("📥 나무위키에서 데이터 가져오는 중...")
    wiki_data = fetch_lostark_classes()

    if not wiki_data:
        print("⚠️ 데이터를 가져오지 못했습니다.")
        return None

    # 텍스트를 문서 단위로 나누기
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([wiki_data])

    # 벡터DB 생성
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_db = Chroma.from_documents(docs, embedding)

    print("✅ 벡터DB 생성 완료!")
    return vector_db

# 벡터DB 로드
vector_db = load_vector_db() if os.getenv("LOAD_VECTOR_DB", "true").lower() == "true" else None

# LangChain 검색 체인 설정
qa_chain = (
    ConversationalRetrievalChain.from_llm(llm, retriever=vector_db.as_retriever(), memory=memory)
    if vector_db
    else None
)

# 챗봇 응답 함수
def get_chat_response(question: str):
    if qa_chain is None:
        return "⚠️ 데이터베이스가 없습니다. 먼저 나무위키 데이터를 불러오세요."
    
    response = qa_chain.invoke({"question": question})
    return response["answer"]

# 챗봇 응답 테스트
if __name__ == "__main__":
    question = "로스트아크의 클래스에 대해 설명해줘"
    response = get_chat_response(question)
    print(response)
