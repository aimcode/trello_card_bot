from pprint import pprint

from trello import TrelloClient

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
API_KEY: str = config.tr_config.api_key
API_SECRET: str = config.tr_config.api_secret

client = TrelloClient(
    api_key=API_KEY,
    api_secret=API_SECRET)

all_boards = client.list_boards()
last_board = all_boards[-1]
list_id = last_board.list_lists()[0].id
my_list = last_board.get_list(list_id)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


def is_forwarded_message(message: Message) -> bool:
    return message.forward_from_chat is not None


card_title = ""


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Трелло-бот\nПерешли мне сообщение и я добавлю его как карточку в трелло')

@dp.message(is_forwarded_message)
async def handle_forwarded_message(message: Message):
    message_link = f"Нажми [сюда](t.me/{message.forward_from_chat.username}/{message.forward_from_message_id}) чтобы перейти по ссылке"
    my_list.add_card(card_title, desc=message_link)
    print(message_link)
    await message.answer(f"Карточка добавленна в Трелло \nЗаголовок: {card_title}\nСсылка на сообщение: {message_link}")

@dp.message()
async def echo_message(message: Message):
    global card_title
    card_title = message.text.upper()
    print(card_title)



if __name__ == '__main__':
    dp.run_polling(bot)
