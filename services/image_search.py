import os
import numpy as np
import pickle
from typing import Optional, List, Dict
from config.settings import Config
from services.embedding_service import EmbeddingService

class ImageSearch:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.image_data = self._load_image_embeddings()
    
    def _load_image_embeddings(self) -> List[Dict]:
        """加载或生成图片嵌入缓存"""
        # 尝试加载缓存
        if os.path.exists(Config.CACHE_FILE):
            try:
                with open(Config.CACHE_FILE, 'rb') as f:
                    return pickle.load(f)
            except (pickle.UnpicklingError, EOFError):
                print("缓存文件损坏，重新生成...")
        
        # 生成新缓存
        image_files = self._get_image_files()
        embeddings = self._generate_embeddings(image_files)
        
        # 保存缓存
        with open(Config.CACHE_FILE, 'wb') as f:
            pickle.dump(embeddings, f)
            
        return embeddings
        
    def _get_image_files(self) -> List[str]:
        """获取图片文件名列表（不含扩展名）"""
        if not os.path.exists(Config.IMAGE_DIR):
            os.makedirs(Config.IMAGE_DIR, exist_ok=True)
            
        return [
            os.path.splitext(f)[0]
            for f in os.listdir(Config.IMAGE_DIR)
            if f.lower().endswith('.png')
        ]
    
    def _generate_embeddings(self, filenames: List[str]) -> List[Dict]:
        """批量生成文件名嵌入"""
        embeddings = []
        for filename in filenames:
            try:
                embedding = self.embedding_service.get_embedding(filename)
                embeddings.append({
                    "filename": f"{filename}.png",
                    "embedding": embedding
                })
            except Exception as e:
                print(f"生成嵌入失败 [{filename}]: {str(e)}")
        return embeddings
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """余弦相似度计算"""
        return np.dot(a, b)
    
    def search(self, query: str, top_k: int = 5) -> List[str]:
        """语义搜索最匹配的图片"""
        try:
            query_embedding = self.embedding_service.get_embedding(query)
        except Exception as e:
            print(f"查询嵌入生成失败: {str(e)}")
            return []
        
        similarities = [
            (img["filename"], self._cosine_similarity(query_embedding, img["embedding"]))
            for img in self.image_data
        ]
        
        if not similarities:
            return []
            
        # 按相似度降序排序并返回前top_k个结果
        sorted_items = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
        return [os.path.join(Config.IMAGE_DIR, item[0]) for item in sorted_items] 