import aiogram
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


class MainFSM(StatesGroup):
    start = State()
    debtors_list = State()


def update_db_on_message(db, msg):
    users = db.users
    if users.count_documents({"_id": msg.from_user.id}) == 0:
        users.insert_one({
            "_id": msg.from_user.id,
            "start_date": msg.date,
            "username": msg.from_user.username,
            "debtors": []
        })

    username_in_base = users.find_one({"_id": msg.from_user.id})["username"]
    if username_in_base != msg.from_user.username:
        users.update_one({"_id": msg.from_user.id},
                         {"$set": {"username": msg.from_user.username}})


PrHa_router = aiogram.Router()


@PrHa_router.message(Command("start"), F.chat.id > 0)
async def on_start(msg, state: FSMContext, db):
    update_db_on_message(db, msg)

    print(msg.message_id)

    r_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Перейти к должникам💵")]])

    await msg.reply("Рады вас приветствовать в нашем боте для учета должников!",
                    reply_markup=r_markup)
    await state.set_state(MainFSM.start)


@PrHa_router.message(F.chat.id > 0, MainFSM.start)
async def debtors_handler(msg, state: FSMContext, db, bot: aiogram.Bot):
    update_db_on_message(db, msg)

    await bot.send_message(chat_id=msg.chat.id, text="Загрузка, подождите...",
                           reply_markup=ReplyKeyboardMarkup(
                               keyboard=[[KeyboardButton(text="Создать должника")]]))

    r_markup = []

    people = db.users.find_one({"_id": msg.from_user.id})["debtors"]

    for p in people:
        r_markup.append([InlineKeyboardButton(text=p["name"], callback_data=p["_id"])])

    if len(r_markup) == 0:
        r_markup = [[InlineKeyboardButton(text="У вас нет должников", callback_data="pass")]]

    r_markup = InlineKeyboardMarkup(inline_keyboard=r_markup)

    await msg.reply("Вот ваши должники:", reply_markup=r_markup)


