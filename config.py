from dataclasses import dataclass

from environs import Env


@dataclass
class TrelloConfig:
    api_key: str
    api_secret: str

@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot
    tr_config: TrelloConfig


# Создаем функцию, которая будет читать файл .env и возвращать экземпляр
# класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        tr_config=TrelloConfig(
            api_key=env('API_KEY'),
            api_secret=env('API_SECRET')
        )
    )