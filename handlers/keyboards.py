from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Показать задачи')],
    [KeyboardButton(text='Добавить задачу')],
    [KeyboardButton(text='Удалить задачу')]
], resize_keyboard=True, input_field_placeholder='Выберите действие')

# inline_key = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Knopka1', callback_data='k1')],
#     [InlineKeyboardButton(text='Knopka2', callback_data='k2')],
#     [InlineKeyboardButton(text='Knopka3', callback_data='k3')]
# ])