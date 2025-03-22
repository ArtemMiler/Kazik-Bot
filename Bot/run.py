import asyncio

from aiogram import Bot, Dispatcher, types

from Bot.config import TOKEN
from Bot.Handlers import bonus_spin, common, spin
from Database import create_tables


async def main():
    await create_tables()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(common.router, spin.router, bonus_spin.router)

    bot_info = await bot.get_me()

    @dp.message(lambda message: message.chat.type in ["group", "supergroup"] and message.new_chat_members)
    async def bot_added_to_group(message: types.Message):
        if any(member.id == bot_info.id for member in message.new_chat_members):
            await message.reply(
                "Спасибо, что добавили меня в группу!🍀\n"
                "Чтобы начать играть, отправьте /start"
            )

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
