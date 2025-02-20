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
            print(f"✅ JSON 데이터 로드 완료! (총 {len(self.documents)}개)")
            print("🔍 로드된 데이터 샘플:", self.documents[:5])

        # ✅ 데이터가 Document 객체인지 확인
        if isinstance(self.documents[0], Document):
            print("✅ 로드된 데이터는 Document 객체입니다.")
        else:
            print("⚠️ 로드된 데이터는 Document 객체가 아닙니다. JSON 구조를 확인하세요.")


    def split_into_chunks(self, chunk_size=300, chunk_overlap=50):
        """ 문서를 작은 청크로 분할하는 메서드 (메타데이터 유지) """
        if not self.documents:
            print(":warning: 로드된 JSON 데이터가 없습니다. `load_documents()`를 먼저 실행하세요.")
            return

        self.split_documents = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        for item in self.documents:
            # ✅ Document 객체인지 확인 후 처리
            if isinstance(item, Document):
                metadata = item.metadata  
            elif isinstance(item, dict):  
                metadata = item
            else:
                print(f"⚠️ 예상치 못한 데이터 타입: {type(item)}")
                continue

            processed_metadata = {
                "id": str(metadata.get("id", "N/A")),
                "관광지명": metadata.get("관광지명", "N/A"),
                "설명": metadata.get("설명", "No description"),
                "위치": metadata.get("소재지도로명주소", metadata.get("소재지지번주소", "정보 없음"))
            }

            document = Document(page_content=f"{processed_metadata['관광지명']}, {processed_metadata['설명']}", metadata=processed_metadata)
            self.split_documents.extend(text_splitter.split_documents([document]))

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
        """ FAISS 벡터 DB를 생성하는 메서드 (메타데이터 유지) """
        if not self.split_documents:
            print(":warning: 분할된 문서가 없습니다. `split_into_chunks()`를 먼저 실행하세요.")
            return

        for doc in self.split_documents:
            print(f"📌 저장 문서 내용: {doc.page_content}, 메타데이터: {doc.metadata}")

        self.vector_db = FAISS.from_documents(self.split_documents, self.embedding_model)
        print("✅ 벡터 DB 생성 완료! (메타데이터 포함)")

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
            self.faiss_index = self.vector_db.index  # 🔹 FAISS 인덱스를 별도로 저장
            print(f"✅ 벡터 DB 로드 완료! (경로: {self.db_path}) | 벡터 개수: {self.faiss_index.ntotal}")
        except Exception as e:
            print(f":warning: 벡터 DB 로드 중 오류 발생: {e}")
            
    def search_similar_locations(self, query, k=5):
        if not self.vector_db:
            print("⚠️ 벡터 DB가 로드되지 않았습니다. `load_vector_db()`를 먼저 실행하세요.")
            return []

        query_vector = self.embedding_model.embed_query(query)
        docs = self.vector_db.similarity_search_by_vector(query_vector, k=k)

        results = []
        for i, doc in enumerate(docs):
            metadata = doc.metadata if hasattr(doc, "metadata") else {}
            results.append({
                "id": metadata.get("id", str(i)),  
                "name": metadata.get("관광지명", "이름 없음"),
                "description": metadata.get("설명", "설명 없음"),
                "location": metadata.get("위치", "정보 없음")  # 위치 추가
            })

        return results

    def get_location_by_id(self, id):
        """ 특정 관광지 ID로 상세 정보 조회 """
        if not self.vector_db:
            print("⚠️ 벡터 DB가 로드되지 않았습니다. `load_vector_db()`를 먼저 실행하세요.")
            return None

        for doc in self.split_documents:
            metadata = doc.metadata if hasattr(doc, "metadata") else {}
            if metadata.get("id") == id:
                return {
                    "name": metadata.get("관광지명", "이름 없음"),
                    "description": metadata.get("설명", "설명 없음"),
                    "location": metadata.get("위치", "정보 없음")
                }

        return None