from aiogram import types, F, Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import engine

import handlers.keyboards as kb
from db import repository

router = Router()


class Task(StatesGroup):
    task_name = State()
    task_id = State()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я ваш личный помощник для управления задачами. Вот что я могу сделать:\n"
                         "1. Показать задачи: Я покажу вам все ваши текущие задачи.\n"
                         "2. Добавить задачу: Напишите мне, что вы хотите сделать, и я добавлю это в ваш список задач.\n"
                         "3. Удалить задачу: Укажите номер задачи, которую вы хотите удалить, и я уберу её из списка.",reply_markup=kb.main)


@router.message(F.text == 'Добавить задачу')
async def read_task(message: types.Message, state: FSMContext):
    await state.set_state(Task.task_name)
    await message.answer("Введите задачу")


@router.message(Task.task_name)
async def add_task(message: types.Message, state: FSMContext):
    await state.update_data(task_name=message.text)
    async with AsyncSession(engine) as session:
        await repository.create_task(session, message.text, "")
    data = await state.get_data()
    await message.answer(f"Задача {data['task_name']} добавлена")
    await state.clear()


@router.message(F.text == 'Удалить задачу')
async def read_task_id(message: types.Message, state: FSMContext):
    await state.set_state(Task.task_id)
    await message.answer("Введите номер задачи:")


@router.message(Task.task_id)
async def delete_task(message: types.Message, state: FSMContext):
    await state.update_data(task_id=message.text)
    async with AsyncSession(engine) as session:
        await repository.delete_todo(int(message.text), session)
    await message.answer(f"Задача под номером {message.text} удалена.")
    await state.clear()

@router.message(F.text == 'Показать задачи')
async def show_tasks(message: types.Message):
    async with AsyncSession(engine) as session:
        tasks = await repository.read_todos(session)
    if not tasks:
        await message.answer("Задачи не найдены.")
        return
    response = "Список задач:\n"
    for task in tasks:
        response += f"Задача №{task.id}: {task.title}\n"
    await message.answer(response)


@router.message()
async def cmd_st(message: types.Message):
    await message.answer("Неверная команда, попробуйте что-нибудь другое")


# @router.message(Command("test1"))
# async def cmd_test1(message: types.Message):
#     await message.answer("Test 1", reply_markup=kb.inline_key)
#
# @router.callback_query(F.data == 'k1')
# async def k1(callback: CallbackQuery):
#     # await callback.answer()
#     await callback.message.answer('Привет!')