from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.cache import Base, PromptCache, ModelCache
from typing import Optional
from pathlib import Path
import shutil

class DatabaseService:
    class ModelStorage:
        """内部类，处理模型文件的存储"""
        def __init__(self, base_path: str = "storage/models"):
            self.base_path = Path(base_path)
            self.base_path.mkdir(parents=True, exist_ok=True)

        def save_model(self, numbers: list[int], model_data: bytes,
                      model_type: str, file_format: str) -> tuple[Path, str]:
            """保存模型文件并返回完整路径和相对路径"""
            numbers_str = "".join(map(str, numbers))
            model_dir = self.base_path / model_type / numbers_str
            model_dir.mkdir(parents=True, exist_ok=True)

            filename = f"model.{file_format}"
            file_path = model_dir / filename

            with open(file_path, 'wb') as f:
                f.write(model_data)

            return file_path, str(file_path.relative_to(self.base_path))

        def get_model_path(self, relative_path: str) -> Optional[Path]:
            """获取模型文件的完整路径"""
            full_path = self.base_path / relative_path
            return full_path if full_path.exists() else None

        def delete_model(self, relative_path: str) -> bool:
            """删除模型文件"""
            full_path = self.base_path / relative_path
            if full_path.exists():
                full_path.unlink()
                return True
            return False

    def __init__(self, database_url: str = "sqlite:///cache.db"):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        self.storage = self.ModelStorage()

    def save_response(self, numbers: list[int], prompt: str, response: str) -> None:
        """保存新的回复到缓存（用于基础的文本响应缓存）"""
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
            print("save_response", response)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_cached_response(self, numbers: list[int], prompt: str) -> Optional[str]:
        """获取缓存的回复（基础版本）"""
        numbers_str = "".join(map(str, numbers))
        session = self.Session()
        try:
            cache = session.query(PromptCache).filter_by(
                numbers=numbers_str,
                prompt=prompt
            ).first()
            res =  cache.response if cache else None
            print("get_cached_response", res)
            return res
        finally:
            session.close()

    def get_full_cached_response(self, numbers: list[int], prompt: str) -> Optional[dict]:
        """获取完整的缓存响应，包括模型数据"""
        numbers_str = "".join(map(str, numbers))
        session = self.Session()
        try:
            cache = session.query(PromptCache).filter_by(
                numbers=numbers_str,
                prompt=prompt
            ).first()

            if not cache:
                return None

            # 获取所有相关的模型
            models_data = []
            for model in cache.models:
                full_path = self.storage.get_model_path(model.file_path)
                if full_path:
                    models_data.append({
                        "type": model.model_type,
                        "format": model.file_format,
                        "path": str(full_path)
                    })

            res =  {
                "response": cache.response,
                "models": models_data
            }
            print("get_full_cached_response", res)
            return res
        finally:
            session.close()

    def save_response_with_model(self, numbers: list[int], prompt: str,
                               response: str, model_data: bytes,
                               model_type: str, file_format: str) -> dict:
        """保存回复和相关模型"""
        numbers_str = "".join(map(str, numbers))
        session = self.Session()
        file_path = None
        relative_path = None

        try:
            # 1. 创建或获取 PromptCache
            prompt_cache = session.query(PromptCache).filter_by(
                numbers=numbers_str,
                prompt=prompt
            ).first()

            if not prompt_cache:
                prompt_cache = PromptCache(
                    numbers=numbers_str,
                    prompt=prompt,
                    response=response
                )
                session.add(prompt_cache)
                session.flush()

            # 2. 保存模型文件
            file_path, relative_path = self.storage.save_model(
                numbers, model_data, model_type, file_format
            )

            # 3. 创建 ModelCache
            model_cache = ModelCache(
                prompt_cache=prompt_cache,
                model_type=model_type,
                file_format=file_format,
                file_path=relative_path
            )

            prompt_cache.models.append(model_cache)
            session.commit()

            res =  {
                "response": response,
                "model_path": str(file_path)
            }
            print("save_response_with_model", res)
            return res

        except Exception as e:
            session.rollback()
            if relative_path:
                self.storage.delete_model(relative_path)
            raise e
        finally:
            session.close()