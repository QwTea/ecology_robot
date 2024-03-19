from aiogram import exceptions

class Checksub:
    
    async def check(self, bot, channelid, user_id, message, buttons):
        try:
            status = await bot.get_chat_member(chat_id=channelid, user_id=user_id)
            status = status.status
        except exceptions.BadRequest as e:
            print(e)
            await message.answer("❌Бот работает только в лс\!")
        else:
            if status in ("left", "kicked"):
                await buttons.none_sub(message)
            return status
