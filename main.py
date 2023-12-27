import aiogram
import configparser
from private_handler import PrHa_router
from init_db import get_db

config = configparser.ConfigParser()

config.read("config.ini")

bot = aiogram.Bot(token=config.get("API", "token"))
dp = aiogram.Dispatcher()


dp.include_routers(PrHa_router)

dp["db"] = get_db(True)


if __name__ == "__main__":
    dp.run_polling(bot)
