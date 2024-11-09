from openai import AsyncOpenAI
from config.model_config import ModelConfig
from services.db_service import DatabaseService

class BaseLLM:
    def __init__(self):
        config = ModelConfig()
        self.client = AsyncOpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_API_BASE
        )
        self.model = config.MODEL_NAME
        self.db_service = DatabaseService()

    async def generate(self, numbers: list[int], prompt: str) -> str:
        # 首先尝试从缓存获取
        cached_response = self.db_service.get_cached_response(numbers, prompt)
        if cached_response:
            return cached_response

        # 如果缓存中没有，则调用模型
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专门帮助用户构建记忆宫殿的助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            response_text = response.choices[0].message.content

            # 保存到缓存
            self.db_service.save_response(numbers, prompt, response_text)

            return response_text
        except Exception as e:
            raise Exception(f"模型调用失败: {str(e)}")