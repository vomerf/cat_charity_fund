from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Благотварительный фонд"
    app_description: str = "Фонд помогает бездомным кошкам"
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
