from platform import machine
from aiogram import types
from modules.config import URLCHANNEL




class Buttons:
    #главная клава
    main_buttons = [
        [
            types.KeyboardButton(text="Главное меню📌")
        ],
        [
            types.KeyboardButton(text="Другое⚙️"),
            types.KeyboardButton(text="О ботеℹ️")
        ]
    ]
    main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=main_buttons)


    #клава с другой инфой

    another_buttons = [
        [
        types.KeyboardButton(text="Связь с создателем📡")
        ],
        [
        types.KeyboardButton(text="В меню◀️")
        ]
    ]
    
    another_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=another_buttons)
    #клава с основным меню
    
    general_buttons = [
    [  
        # types.KeyboardButton(text="Дешевая вода💧"),
        types.KeyboardButton(text="Получить источники🌱", request_location=True)
    ],
    # [
    #     types.KeyboardButton(text="Скидка на кофе☕️"),
    #     # types.KeyboardButton(text="Пункты приемов🌍")
    # ],
        [types.KeyboardButton(text="В меню◀️")]
    
    ]
    
    general_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=general_buttons)
    
    check_sub_button =  [
        [
            types.InlineKeyboardButton(text="я подписался", callback_data="sub")
        ]
    ]
    
    
    сheck_sub_keyboard = types.InlineKeyboardMarkup(inline_keyboard=check_sub_button)
    
    source_button = [
    [  
        types.KeyboardButton(text="Бесплатная вода🌱")
    ],
    [
        types.KeyboardButton(text="Скидка на кофе☕️"),
    ],
        [types.KeyboardButton(text="В меню◀️")]
    
    ]
    
    source_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=source_button)
    #Пункты приемов клава
    
    # reception_points = [
    # [
    #     types.KeyboardButton(text="Пункты приема металла🔧"),
    #     types.KeyboardButton(text="Пункты приема стекла🪞")
    # ],
    # [
    #     types.KeyboardButton(text="Пункты приема бумаги📃")
    # ],
    # [
    #     types.KeyboardButton(text="В меню◀️")
    # ]
    
    # ]
    
    # reception_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=reception_points)

    place_button = [
        [
            types.InlineKeyboardButton(text="показать на карте", callback_data="place")
        ]
    ]
    place_keyboard = types.InlineKeyboardMarkup(inline_keyboard=place_button)
    place_coffee_button = [
        [
            types.InlineKeyboardButton(text="показать на карте", callback_data="place coffee")
        ]
    ]
    place_coffee_keyboard = types.InlineKeyboardMarkup(inline_keyboard=place_coffee_button)
    async def main_button(self, message):
        
        await message.answer(f"*Привет\!*\n\n🍃Мы поможем вам легко и быстро найти бесплатные источники воды, взамен на вашу помощь в сохранении экологии\!", reply_markup=self.main_keyboard)

    async def none_sub(self, message):
        await message.answer(f"*Привет\!*\n🍃Мы поможем вам легко и быстро найти бесплатные источники воды, взамен на вашу помощь в сохранении экологии\! \n\n_Для работы нужно быть подписанным на наш [телеграм канал]({URLCHANNEL})\!_\n\nТам мы рассказываем многое о Экологии и как она уже сейчас меняет нашу жизнь\!", reply_markup=self.сheck_sub_keyboard)

    async def another_button(self, message):
        await message.reply("Ты находишься в меню с иной инофрмацией💨", reply_markup=self.another_keyboard)

    async def back_button(self, message):
        await message.reply("Перехожу в меню\.\.\.", reply_markup=self.main_keyboard)
    
    # async def reception_func(self, message):
    #     await message.reply("Выбери тип вторичного сырья который ты хочешь сдать👇", reply_markup=self.reception_keyboard)
        
    async def basic_menu(self, message):
        await message.reply("Перехожу в главное меню\.\.\.", reply_markup=self.general_keyboard)
    
    async def about_bot(self, message):
        await message.reply("Не сделано")
    
    async def connection_owner(self, message):
        await message.reply("Telegram создателя \- @tea\_official")
    
    async def chip_water(self, message):
        await message.reply("Не сделано")
    
    async def free_water(self, message):
        await message.reply("Сделано при поддержке [Твоя вода](tvojavoda.ru)")
        
    
    async def sale_coffee(self, message):
        await message.reply("Не сделано")
        

    # async def reception_metal(self, message):
    #     await message.reply("Не сделано")
        
    # async def reception_paper(self, message):
    #     await message.reply("Не сделано")
        
    # async def reception_glass(self, message):
    #     await message.reply("Не сделано")
        
    
        
