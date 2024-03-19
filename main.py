
from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram import F
from numpy import source
from modules.buttons import *
from modules.database import *
from modules.check_sub import *
from modules.water import *
from modules.config import TOKEN, CHANNELID, DBPATH
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode="MarkdownV2")

#конструктор класса кнопок
buttons = Buttons()

#конструктор класса базы данных
moduledb = Database()

#конструктор проверки подписки на канал
checksub = Checksub()

#конструктор класса поиска корриднаты
water = Getting_location()

#класс состояния FSM для запроса данных
class Geo(StatesGroup):
    geo_message = State()
    source_type = State()
    
locations_data = asyncio.run(water.get_from_db(DBPATH))

@dp.message(Command(commands=["start"]))
async def command_start_handler(message: Message):
    status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
    if status_user not in ("left", "kicked", None):
        await buttons.main_button(message)
        value_users = await moduledb.check_to_db(message.chat.id, DBPATH)
        if value_users == None:
            await moduledb.add_to_db(message.chat.id, message.chat.username, message.chat.last_name, message.chat.first_name, DBPATH)
        else:
            pass
@dp.message(F.content_type.in_({"location"}))
async def handle_location(message: types.location, state: FSMContext):
    status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
    if status_user not in ("left", "kicked", None):
        await message.reply("Что вы хотите получить?", reply_markup=buttons.source_keyboard)
        await state.set_state(Geo.geo_message)
        await state.update_data(geo_message=message)
        await state.set_state(Geo.source_type)
    # status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
    # if status_user not in ("left", "kicked", None):
    #     print(message)
    #     lat = message.location.latitude
    #     lon = message.location.longitude
    #     location = await water.get_location(latitude=lat, longitude=lon, DBPATH=DBPATH)
    #     for_send_location = location[:3]
    #     for i in for_send_location:
    #         try:
    #             place = await moduledb.get_places_row(DBPATH, id=i)
    #             photo = place[8]
    #             place_keyboard = buttons.place_keyboard
    #             await message.answer_photo(photo=photo, caption=f"{place[0]}\n\n💧{place[4]}\n\nОписание:\n{place[2]}\n\n📍{place[3]}", parse_mode=None, reply_markup=place_keyboard)
    #         except TelegramBadRequest:
    #             await message.answer(f"{place[0]}\n💧{place[4]}\n\nОписание:\n{place[2]}\n\n📍{place[3]}", parse_mode=None, reply_markup=place_keyboard)

@dp.message(Geo.source_type)
async def choice_source(message: Message, state: FSMContext):
    if message.text == "Бесплатная вода🌱":
        await state.update_data(source_type=message.text)
        location_message = await state.get_data()
        location_message = location_message["geo_message"]
        lat = location_message.location.latitude
        lon = location_message.location.longitude
        location = await water.get_location(latitude=lat, longitude=lon, DBPATH=DBPATH)
        for_send_location = location[:3]
        for i in for_send_location:
            try:
                place = await moduledb.get_places_row(DBPATH, id=i)
                photo = place[8]
                place_keyboard = buttons.place_keyboard
                await message.answer_photo(photo=photo, caption=f"{place[0]}\n\nБесплатная вода🚰\n\n💧{place[4]}\n\nОписание:\n{place[2]}\n\n📍{place[3]}", parse_mode=None, reply_markup=place_keyboard)
            except TelegramBadRequest:
                await message.answer(f"{place[0]}\n\nБесплатная вода🚰\n💧{place[4]}\n\nОписание:\n{place[2]}\n\n📍{place[3]}", parse_mode=None, reply_markup=place_keyboard)
        await state.clear()
        await message.answer("*Готово\!*\n\nЯ отправил тебе самые близжайшие точки\!", reply_markup=buttons.main_keyboard)
    elif message.text == "Скидка на кофе☕️":
        location_message = await state.update_data(source_type=message.text)
        location_message = location_message["geo_message"]
        lat = location_message.location.latitude
        lon = location_message.location.longitude
        location = await water.get_location_coffee(latitude=lat, longitude=lon, DBPATH=DBPATH)
        for_send_location = location[:3]
        for i in for_send_location:
            try:
                place = await moduledb.get_places_row_coffee(DBPATH, id=i)
                photo = place[8]
                place_keyboard = buttons.place_coffee_keyboard
                await message.answer_photo(photo=photo, caption=f"{place[0]}\n\nСкидка на кофе ☕️\n\n{place[5]}\n\nОписание:\n{place[2]}\n\n📍{place[3]}", parse_mode=None, reply_markup=place_keyboard)
            except TelegramBadRequest:
                await message.answer(f"{place[0]}\n\nСкидка на кофе ☕️\n\n{place[5]}\n\nОписание:\n{place[2]}\n\n📍{place[3]}", parse_mode=None, reply_markup=place_keyboard)
        await state.clear()
        await message.answer("*Готово\!*\n\nЯ отправил тебе самые близжайшие точки\!", reply_markup=buttons.main_keyboard)
    elif message.text == "В меню◀️":
        await state.clear()
        await buttons.back_button(message)
    else:
        await message.reply("Не знаю такого\!\n\nЧтобы выйти нажмите В меню◀️")
    
@dp.callback_query(Text(text="place"))
async def send_random_value(callback: types.CallbackQuery):
    street = callback.message.caption.split("📍")[1]
    geo = await moduledb.get_geo(DBPATH, street)
    await callback.message.reply_location(geo[0], geo[1])
@dp.callback_query(Text(text="sub"))
async def checking_subscripe_for_channel(callback: types.CallbackQuery):
    status_user = await checksub.check(bot, CHANNELID, callback.message.chat.id, callback.message, buttons)
    if status_user not in ("left", "kicked", None):
        await callback.message.answer("Ура\! Вы подписаны на канал\!")
        await buttons.main_button(callback.message)
    else:
        await callback.message.answer("Вы не подписаны на канал\!\n\nПодпишитесь и нажмите кнопку еще раз\!")
        
@dp.callback_query(Text(text="place coffee"))
async def send_random_value(callback: types.CallbackQuery):
    street = callback.message.caption.split("📍")[1]
    geo = await moduledb.get_geo_coffee(DBPATH, street)
    await callback.message.reply_location(geo[0], geo[1])



@dp.message(Text(text="В меню◀️"))
async def with_puree(message: types.Message):
    status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
    if status_user not in ("left", "kicked", None):
        await buttons.back_button(message)

@dp.message(Text(text="Главное меню📌"))
async def with_puree(message: types.Message):
    status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
    if status_user not in ("left", "kicked", None):
        await buttons.basic_menu(message)

@dp.message(Text(text="Другое⚙️"))
async def with_puree(message: types.Message):
    status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
    if status_user not in ("left", "kicked", None):
        await buttons.another_button(message)

@dp.message(Text(text="О ботеℹ️"))
async def with_puree(message: types.Message):
    status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
    if status_user not in ("left", "kicked", None):
        await buttons.about_bot(message)

@dp.message(Text(text="Связь с создателем📡"))
async def with_puree(message: types.Message):
    status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
    if status_user not in ("left", "kicked", None):
        await buttons.connection_owner(message)


@dp.message(Text(text="Дешевая вода💧"))
async def with_puree(message: types.Message):
    status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
    if status_user not in ("left", "kicked", None):
        await buttons.chip_water(message)
        
# @dp.message(Text(text="Бесплатная вода🌱"))
# async def with_puree(message: types.Message):
#     status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
#     if status_user not in ("left", "kicked", None):
#         await buttons.free_water(message)
        
# @dp.message(Text(text="Скидка на кофе☕️"))
# async def with_puree(message: types.Message):
#     status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
#     if status_user not in ("left", "kicked", None):
#         await buttons.sale_coffee(message)

# @dp.message(Text(text="Пункты приемов🌍"))
# async def with_puree(message: types.Message):
#     status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
#     if status_user not in ("left", "kicked", None):
#         await buttons.reception_func(message)
    
# @dp.message(Text(text="Пункты приема металла🔧"))
# async def with_puree(message: types.Message):
#     status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
#     if status_user not in ("left", "kicked", None):
#         await buttons.reception_metal(message)
    
# @dp.message(Text(text="Пункты приема стекла🪞"))
# async def with_puree(message: types.Message):
#     status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
#     if status_user not in ("left", "kicked", None):
#         await buttons.reception_glass(message)

# @dp.message(Text(text="Пункты приема бумаги📃"))
# async def with_puree(message: types.Message):
#     status_user = await checksub.check(bot, CHANNELID, message.chat.id, message, buttons)
#     if status_user not in ("left", "kicked", None):
#         await buttons.reception_paper(message)

def main():
    asyncio.run((moduledb.create_db(base_path=DBPATH)))
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
    
    
# from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


# def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
#     """
#     Создаёт реплай-клавиатуру с кнопками в один ряд
#     :param items: список текстов для кнопок
#     :return: объект реплай-клавиатуры
#     """
#     row = [KeyboardButton(text=item) for item in items]