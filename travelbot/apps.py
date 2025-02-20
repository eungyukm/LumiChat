import os
from django.apps import AppConfig
from .utils import VectorDBManager


class YourAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "travelbot"

    def ready(self):
        """앱이 로드될 때 벡터 DB를 자동으로 로드 또는 생성"""
        if os.environ.get("RUN_MAIN") == "true":  
            print("🚀 벡터 DB 자동 로드 또는 생성 시작...")

            db_manager = VectorDBManager()

            if os.path.exists(db_manager.db_path):
                db_manager.load_vector_db()
            else:
                db_manager.load_documents()
                db_manager.split_into_chunks()
                db_manager.generate_embeddings()
                db_manager.create_vector_db()
                db_manager.save_vector_db()

            print("✅ 벡터 DB 설정 완료!")