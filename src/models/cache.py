from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class PromptCache(Base):
    __tablename__ = 'prompt_cache'

    id = Column(Integer, primary_key=True)
    numbers = Column(String, nullable=False)  # 存储数字序列，如 "1234"
    prompt = Column(Text, nullable=False)     # 完整的 prompt
    response = Column(Text, nullable=False)   # 模型的回复
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<PromptCache(numbers={self.numbers}, prompt={self.prompt[:50]}...)>"