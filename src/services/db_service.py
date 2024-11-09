from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.cache import Base, PromptCache
from typing import Optional
from contextlib import contextmanager

class DatabaseService:
    def __init__(self, database_url: str = "sqlite:///cache.db"):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def get_cached_response(self, numbers: list[int], prompt: str) -> Optional[str]:
        """获取缓存的回复"""
        numbers_str = "".join(map(str, numbers))
        session = self.Session()
        try:
            cache = session.query(PromptCache).filter_by(
                numbers=numbers_str,
                prompt=prompt
            ).first()
            response = cache.response if cache else None
            session.expunge_all()  # 分离所有对象
            return response
        finally:
            session.close()

    def save_response(self, numbers: list[int], prompt: str, response: str) -> None:
        """保存新的回复到缓存"""
        numbers_str = "".join(map(str, numbers))
        session = self.Session()
        try:
            # 检查是否已存在相同的记录
            existing = session.query(PromptCache).filter_by(
                numbers=numbers_str,
                prompt=prompt
            ).first()

            if existing:
                existing.response = response
            else:
                cache = PromptCache(
                    numbers=numbers_str,
                    prompt=prompt,
                    response=response
                )
                session.add(cache)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()