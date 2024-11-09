from pydantic_settings import BaseSettings

class ModelConfig(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    MODEL_NAME: str = "gpt-4"

    class Config:
        env_file = ".env"

if __name__ == "__main__":
    config = ModelConfig()
    print(config.OPENAI_API_KEY)
    print(config.OPENAI_API_BASE)
    print(config.MODEL_NAME)