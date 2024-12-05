from aiogram.types import Message
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from states import newariza  # Import qilingan newariza klassini ishlatish

async def start_command(message: Message, bot: Bot):
    await message.answer('Botdan foydalanishni bilmasangiz, /help buyrug\'ini yuboring.')

async def help_command(message: Message, bot: Bot):
    matn = """Botdan foydalanish:
    /new = yangi ariza yuborish,
    /stop = arizani bekor qilish,
    """
    await message.answer(matn)

async def new_command(message: Message, bot: Bot, state: FSMContext):
    await message.answer('To\'liq familiya va ismingizni kiriting:')
    await state.set_state(newariza.name)  # Holatni to'g'ri o'rnating

async def stop_command(message: Message, bot: Bot, state: FSMContext):
    this_state = await state.get_state()
    if this_state is None:
        await message.answer('Bekor qilish uchun ariza mavjud emas.')
    else:
        await state.clear()
        await message.answer('Ariza bekor qilindi!')

async def newarizar_name(message: Message, bot: Bot, state: FSMContext):
    if len(message.text.split()) == 2:
        if not any(char.isdigit() for char in message.text):  # Raqamlarni tekshirish
            await state.update_data(name=message.text)
            await message.answer(f'Ism-familiya kiritildi! \n{message.text}')
            await message.answer("Menga yoshingizni yuboring.")
            await state.set_state(newariza.age)  # Yoshingizni so'rash holatiga o'ting
        else:
            await message.answer("Ism-familiyada raqam qatnashishi mumkin emas.")
    else:
        await message.answer("Iltimos, faqat ism-familiya yuboring va u 2 harfdan ko'proq bo'lishi kerak!")

async def newariza_age(message: Message, bot: Bot, state: FSMContext):
    if message.text.isdigit():
        age1 = int(message.text)
        if 5 < age1 < 120:
            await state.update_data(age=age1)
            await message.answer(f"Yoshingiz {age1} sifatida qabul qilindi.")
            await message.answer("Telefon raqamingizni yuboring:")
            await state.set_state(newariza.phone)  # Telefon raqami so'roviga o'ting
        else:
            await message.answer("Iltimos, yoshingizni 5 va 120 orasida kiriting.")
    else:
        await message.answer("Yoshingizni faqat raqamlar bilan kiriting, masalan: 25.")

async def newariza_phone(message: Message, bot: Bot, state: FSMContext):
    if message.text.isdigit() and len(message.text) in [9, 12]:  # Telefon raqam uzunligi 9 yoki 12 bo'lishi kerak
        await state.update_data(phone=message.text)
        await message.answer(f"Telefon raqamingiz qabul qilindi: {message.text}")
        await message.answer("Ish joyingiz yoki kasbingizni yuboring:")
        await state.set_state(newariza.job)
    else:
        await message.answer("Iltimos, to'g'ri telefon raqamini kiriting (faqat raqamlar, uzunligi 9 yoki 12 bo'lsin).")

async def newariza_job(message: Message, bot: Bot, state: FSMContext):
    if len(message.text) >= 3:  # Ish joyi/kasbi kamida 3 ta harf bo'lishi kerak
        await state.update_data(job=message.text)
        await message.answer(f"Ish joyingiz/kasbingiz qabul qilindi: {message.text}")
        await message.answer("arizadan maqsadingizni yuboring:")
        await state.set_state(newariza.goal)  # Keyingi holatga o'tish
    else:
        await message.answer("Iltimos, ish joyingiz yoki kasbingizni to'liqroq yozing (kamida 3 ta harf bo'lsin).")

async def newariza_goal(message: Message, bot: Bot, state: FSMContext):
    if len(message.text) >= 4:  # Maqsad kamida 4 ta harfdan iborat bo'lishi kerak
        await state.update_data(goal=message.text)
        await message.answer(f"Maqsadingiz qabul qilindi: {message.text}\n\nArizangiz muvaffaqiyatli yakunlandi!")
        await message.answer("Arizangizni tasdiqlash uchun 'ha' deb yozing yoki bekor qilish uchun /stop buyrug'ini yuboring.")
        await state.set_state(newariza.verify)  # Keyingi holatga o'tish
    else:
        await message.answer("Iltimos, maqsadingizni to'liqroq yozing (kamida 4 ta harf bo'lsin).")
        await state.set_state(newariza.goal)

async def newariza_verify(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == "ha":
        data = await state.get_data()
        ariza = (f"To'liq ma'lumotlar:\n"
                 f"Ism-familiya: {data['name']}\n"
                 f"Yosh: {data['age']}\n"
                 f"Telefon: {data['phone']}\n"
                 f"Username: @{message.from_user.username}\n"
                 f"Ish joyi/kasb: {data['job']}\n"
                 f"Maqsad: {data['goal']}")
        await bot.send_message(5812191024, f"Yangi ariza:\n\n{ariza}")
        await message.answer("Arizangiz qabul qilindi ✅")
        await state.clear()  # Holatni tozalash
    else:
        await message.answer("Arizani yuborishni hohlasangiz 'ha' so'zini yuboring. Bekor qilishni istasangiz /stop buyrug'ini yuboring.")
