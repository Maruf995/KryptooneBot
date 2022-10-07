from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handler import fsmKrypto


def callback(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_2 = InlineKeyboardButton("Next", callback_data="button_call_1")
    markup.add(button_call_2)


    def register_callback_handler(dp: Dispatcher):
        dp.register_callback_query_handler(callback, lambda call: call.data == "button_call_1")

