# utils/vector_store.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import json
import os

# utils.py
import os


class JobVectorStore:
    def __init__(self, lazy_load=True):
        """
        lazy_load=True: 初始化时不加载模型，避免网络问题
        """
        self.embeddings = None
        self.lazy_load = lazy_load
        if not lazy_load:
            self._init_embeddings()

    def _init_embeddings(self):
        """真正需要时才初始化"""
        if self.embeddings is not None:
            return
        try:
            # 设置国内镜像（可选）
            os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

            # 根据你的 langchain 版本选择正确导入
            try:
                from langchain_huggingface import HuggingFaceEmbeddings
            except ImportError:
                from langchain_community.embeddings import HuggingFaceEmbeddings

            self.embeddings = HuggingFaceEmbeddings(
                model_name="shibing624/text2vec-base-chinese",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        except Exception as e:
            print(f"⚠️ 向量模型加载失败（可忽略）: {e}")
            self.embeddings = None

    def add_jobs(self, jobs):
        # 使用前确保初始化
        self._init_embeddings()
        # ... 原有逻辑

    def search(self, query, k=5):
        self._init_embeddings()
        # ... 原有逻辑