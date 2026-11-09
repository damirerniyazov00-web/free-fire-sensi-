import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Tokeningizni shu yerga yozing
TOKEN = "8965175814:AAF7YkTac_AJILNrpmwLt5paliwE2JumdzU"
ADMIN_IDS = [904227416] # O'z Telegram ID raqamingizni yozing

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Asosiy menyu
def main_menu(user_id):
    keyboard_buttons = [
        [InlineKeyboardButton(text="📱 Telefon modeliga ko'ra Nastroyka", callback_data="select_phone")],
        [InlineKeyboardButton(text="🌐 Barcha nastroykalar sayti", url="https://sensiaipro.online/")],
        [InlineKeyboardButton(text="🎯 Umumiy Headshot Nastroyka", callback_data="show_headshot")]
    ]
    
    if user_id in ADMIN_IDS:
        keyboard_buttons.append([InlineKeyboardButton(text="⚙️ Admin Panel", callback_data="admin_panel")])
        
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

# FSM holati - Telefon nomini qidirish uchun
class PhoneSearchState(StatesGroup):
    waiting_for_phone_name = State()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        f"Salom, **{message.from_user.first_name}**! 🔥\n\n"
        "Free Fire o'yinida har qanday telefon uchun eng zo'r **Headshot nastroyka, DPI va Sezgirlikni** topish uchun quyidagi tugmani bosing yoki o'z telefon modelingizni yozing:"
    )
    await message.answer(text, reply_markup=main_menu(message.from_user.id), parse_mode="Markdown")

# Telefon modeli bo'yicha qidirishni boshlash
@dp.callback_query(F.data == "select_phone")
async def ask_phone_model(callback: CallbackQuery, state: FSMContext):
    text = (
        "🔍 **Telefon modelingizni yozib yuboring**\n"
        "(Masalan: *Samsung A52, Redmi Note 10, iPhone 11, Poco X3* va hokazo):\n\n"
        "Yoki to'g'ridan-to'g'ri rasmiy saytdan qidirish uchun bosing: [Sensiai Pro](https://sensiaipro.online/)"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Saytga o'tish", url="https://sensiaipro.online/")],
        [InlineKeyboardButton(text="◀️ Ortga", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await state.set_state(PhoneSearchState.waiting_for_phone_name)
    await callback.answer()

# Foydalanuvchi yozgan telefon modeli bo'yicha javob qaytarish
@dp.message(PhoneSearchState.waiting_for_phone_name)
async def process_phone_name(message: Message, state: FSMContext):
    phone_name = message.text
    await state.clear()
    
    text = (
        f"📱 **{phone_name}** uchun Free Fire nastroykalari:\n\n"
        f"Siz izlagan model va barcha turdagi telefonlar uchun eng so'nggi va aniq sozlamalarni quyidagi havola orqali olishingiz mumkin:\n\n"
        f"🔗 **Rasmiy baza:** [Sensiai Pro Sayti](https://sensiaipro.online/)\n\n"
        f"💡 *Maslahat:* Saytga kirib o'z telefon modelingizni qidiring va u yerdagi DPI hamda General (Обзор) foizlarini o'rnating!"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Nastroykani olish (Saytga kirish)", url="https://sensiaipro.online/")],
        [InlineKeyboardButton(text="🔄 Boshqa telefonni qidirish", callback_data="select_phone")],
        [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_menu")]
    ])
    await message.answer(text, reply_markup=kb, parse_mode="Markdown", disable_web_page_preview=True)

@dp.callback_query(F.data == "show_headshot")
async def show_headshot(callback: CallbackQuery):
    text = (
        "🎯 **Universal Headshot Nastroyka:**\n\n"
        "• **General:** 95 - 100\n"
        "• **Red Dot:** 90 - 95\n"
        "• **2x Scope:** 88\n"
        "• **4x Scope:** 90\n"
        "• **AWM Scope:** 50\n"
        "• **Free Look:** 60\n\n"
        "Boshqa telefon modellari uchun maxsus nastroykalarni quyidagi saytdan olasiz:"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Sensiaipro.online ga o'tish", url="https://sensiaipro.online/")],
        [InlineKeyboardButton(text="◀️ Ortga", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown", disable_web_page_preview=True)
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Asosiy menyu:", 
        reply_markup=main_menu(callback.from_user.id), 
        parse_mode="Markdown"
    )
    await callback.answer()

# Botni ishga tushirish
async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
