from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class PromptCache(Base):
    __tablename__ = 'prompt_cache'

    id = Column(Integer, primary_key=True)
    numbers = Column(String, nullable=False, index=True)  # 添加索引以提高查询性能
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # 建立与模型缓存的一对多关系
    models = relationship("ModelCache", back_populates="prompt_cache", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PromptCache(numbers={self.numbers}, prompt={self.prompt[:50]}...)>"

class ModelCache(Base):
    __tablename__ = 'model_cache'

    id = Column(Integer, primary_key=True)
    prompt_cache_id = Column(Integer, ForeignKey('prompt_cache.id'), nullable=False)
    model_type = Column(String, nullable=False)    # 例如: "image", "3d_model"
    file_format = Column(String, nullable=False)   # 例如: "png", "glb", "fbx"
    file_path = Column(String, nullable=False)     # 存储文件的相对路径
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # 建立与提示缓存的多对一关系
    prompt_cache = relationship("PromptCache", back_populates="models")

    def __repr__(self):
        return f"<ModelCache(prompt_id={self.prompt_cache_id}, type={self.model_type})>"

    @property
    def numbers(self):
        """通过关系获取数字序列"""
        return self.prompt_cache.numbers if self.prompt_cache else None

    @property
    def description(self):
        """通过关系获取描述"""
        return self.prompt_cache.response if self.prompt_cache else None