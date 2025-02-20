import os
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from tqdm import tqdm


class VectorDBManager:
    def __init__(self, json_path="Datas/traveldata.json", db_path="vector_db"):
        """ 벡터 DB 관리 클래스 초기화 """
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print(":warning: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다. .env 파일에 API 키를 설정해주세요.")
            exit()
        self.json_path = os.path.join(os.getcwd(), json_path)
        self.db_path = db_path
        self.documents = []
        self.split_documents = []
        self.embedding_model = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.vector_db = None

    def load_documents(self):
        """ JSON 파일에서 데이터를 로드하는 메서드 """
        if not os.path.exists(self.json_path):
            print(f":warning: JSON 파일이 존재하지 않습니다: {self.json_path}")
            return

        loader = JSONLoader(file_path=self.json_path, jq_schema=".records[]", text_content=False)
        self.documents = loader.load()

        if not self.documents:
            print(":warning: JSON 데이터가 비어 있습니다.")
        else:
            print(f"✅ JSON 데이터 로드 완료!")

    def split_into_chunks(self, chunk_size=300, chunk_overlap=50):
        """ 문서를 작은 청크로 분할하는 메서드 """
        if not self.documents:
            print(":warning: 로드된 JSON 데이터가 없습니다. `load_documents()`를 먼저 실행하세요.")
            return

        docs = [
            f"{item.metadata.get('관광지명', 'N/A')}, {item.metadata.get('설명', 'No description')}"
            if isinstance(item, Document) else
            f"{item.get('관광지명', 'N/A')}, {item.get('설명', 'No description')}"
            for item in self.documents
            ]
        document_objs = [Document(page_content=text) for text in docs]

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.split_documents = text_splitter.split_documents(document_objs)
        print(f"✅ 문서 분할 완료! (총 {len(self.split_documents)}개)")

    def generate_embeddings(self):
        """ 분할된 문서에 대해 임베딩을 생성하는 메서드 """
        if not self.split_documents:
            print(":warning: 분할된 문서가 없습니다. `split_into_chunks()`를 먼저 실행하세요.")
            return []

        embeddings = self.embedding_model.embed_documents(
            [doc.page_content for doc in tqdm(self.split_documents, desc=":arrows_counterclockwise: 임베딩 생성 중...")]
        )
        print(f"✅: 임베딩 생성 완료! (총 {len(embeddings)}개)")
        return embeddings

    def create_vector_db(self):
        """ FAISS 벡터 DB를 생성하는 메서드 """
        if not self.split_documents:
            print(":warning: 분할된 문서가 없습니다. `split_into_chunks()`를 먼저 실행하세요.")
            return

        self.vector_db = FAISS.from_documents(self.split_documents, self.embedding_model)
        print("✅ 벡터 DB 생성 완료!")

    def save_vector_db(self):
        """ 생성된 FAISS 벡터 DB를 로컬에 저장하는 메서드 """
        if self.vector_db:
            self.vector_db.save_local(self.db_path)
            print(f"✅ 벡터 DB 저장 완료! (경로: {self.db_path})")
        else:
            print(":warning: 저장할 벡터 DB가 없습니다. 먼저 `create_vector_db()`를 실행하세요.")

    def load_vector_db(self):
        """ 기존 FAISS 벡터 DB를 로드하는 메서드 """
        if not os.path.exists(self.db_path):
            print(":warning: 로드할 벡터 DB가 없습니다. 먼저 `create_vector_db()`를 실행하세요.")
            return

        try:
            self.vector_db = FAISS.load_local(self.db_path, self.embedding_model, allow_dangerous_deserialization=True)
            print(f"✅ 벡터 DB 로드 완료! (경로: {self.db_path})")
        except Exception as e:
            print(f":warning: 벡터 DB 로드 중 오류 발생: {e}")


if __name__ == "__main__":
    # VectorDBManager 인스턴스 생성
    db_manager = VectorDBManager()

    # 1. JSON 데이터 로드
    db_manager.load_documents()

    # 2. 문서 분할
    db_manager.split_into_chunks()

    # 3. 임베딩 생성 (시간이 다소 걸릴 수 있습니다)
    db_manager.generate_embeddings()

    # 4. 벡터 DB 생성
    db_manager.create_vector_db()

    # 5. 벡터 DB 저장
    db_manager.save_vector_db()

    # 6. 저장된 벡터 DB 로드 (테스트)
    db_manager.load_vector_db()

    print("\n:white_check_mark: 모든 과정이 완료되었습니다.") 