from aiogram import Bot, Dispatcher
from asyncio import run
from aiogram.types import BotCommand
from aiogram.filters import Command, StateFilter

import funksiyalar
import states

dp = Dispatcher()

async def start():
    dp.message.register(funksiyalar.start_command, Command("start"))
    dp.message.register(funksiyalar.help_command, Command("help"))
    dp.message.register(funksiyalar.new_command, Command("new"))
    dp.message.register(funksiyalar.stop_command, Command("stop"))
    dp.message.register(funksiyalar.newarizar_name, StateFilter(states.newariza.name))
    dp.message.register(funksiyalar.newariza_age, StateFilter(states.newariza.age))
    dp.message.register(funksiyalar.newariza_phone, StateFilter(states.newariza.phone))
    dp.message.register(funksiyalar.newariza_job, StateFilter(states.newariza.job))
    dp.message.register(funksiyalar.newariza_goal, StateFilter(states.newariza.goal))
    dp.message.register(funksiyalar.newariza_verify, StateFilter(states.newariza.verify))

    bot = Bot(token="7871849103:AAEHASnzvCB8pVuhOQTiTEbjffiopRmIKj0")
    await dp.start_polling(bot)
    await bot.set_my_commands([
        BotCommand(command='/new' ,description='yangi ariza yuborish '),
        BotCommand(command='/stop' ,description='arizani bekor qilish '),
        BotCommand(command='/help' ,description='botdan foydalanishda yordam '),
    ])

run(start())
