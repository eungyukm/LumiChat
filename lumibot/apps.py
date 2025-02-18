from django.apps import AppConfig
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import requests
from bs4 import BeautifulSoup


class LumibotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lumibot"

    def ready(self):
        """앱이 시작될 때 벡터 DB를 로드합니다."""
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            raise ValueError("⚠️ OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

        # LLM 설정
        self.llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, openai_api_key=openai_api_key)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # 벡터 DB 로드
        self.vector_db = self.load_vector_db()
        
        # 검색 체인 생성
        if self.vector_db:
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                self.llm, retriever=self.vector_db.as_retriever(), memory=self.memory
            )
        else:
            self.qa_chain = None

    def fetch_lostark_classes(self):
        """나무위키에서 로스트아크 클래스 정보를 가져옵니다."""
        url = "https://namu.wiki/w/%EB%A1%9C%EC%8A%A4%ED%8A%B8%EC%95%84%ED%81%AC/%ED%81%B4%EB%9E%98%EC%8A%A4"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ 요청 실패: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.get_text(separator="\n", strip=True)
        return content

    def load_vector_db(self):
        """벡터 DB를 로드하거나 새로 생성합니다."""
        print("📥 나무위키에서 데이터 가져오는 중...")
        wiki_data = self.fetch_lostark_classes()

        if not wiki_data:
            print("⚠️ 데이터를 가져오지 못했습니다.")
            return None

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.create_documents([wiki_data])

        embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vector_db = Chroma.from_documents(docs, embedding)

        print("✅ 벡터DB 생성 완료!")
        return vector_db