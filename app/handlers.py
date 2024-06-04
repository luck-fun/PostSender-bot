import asyncio
import app.keyboards as keyboards

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from database.tables import cursor
from database.methods import Methods

router = Router()

class Post(StatesGroup):
    send_post = State()

class Channel(StatesGroup):
    get_channel = State()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Welcome to PostSender bot! This bot was created to make safety to your telegram channel", reply_markup=keyboards.main_keyboard)

@router.message(F.text == "Add channel")
async def add_channel(message: Message, state: FSMContext):
    selected_channel = cursor.execute("SELECT channel_id FROM main_table WHERE user_id = ?", [message.from_user.id]).fetchone()
    if selected_channel != None:
        await message.answer("You already have a channel")
    if selected_channel == None:
        await state.set_state(Channel.get_channel)
        await message.answer("Enter id of your channel")

@router.message(Channel.get_channel)
async def get_channel_id(message: Message, state: FSMContext):
        await state.update_data(channel = message.text)
        data = await state.get_data()
        Methods(message.from_user.id, message.from_user.first_name, data["channel"]).add_channel()
        await message.answer(f"From now on, messages sent to the bot by you via the 'Send post' button will also be sent to the channel with the ID: {data['channel']} \n **Note: This bot must have access to messages in your channel**")
        await state.clear()

@router.message(F.text == "My channel")
async def my_channel(message: Message):
    selected_channel = cursor.execute("SELECT channel_id FROM main_table WHERE user_id = ?", [message.from_user.id]).fetchone()
    if selected_channel == None:
        await message.answer("You haven't a channel")
    else:
        await message.answer(f"Your channel id: {selected_channel}")

@router.message(F.text == "Remove channel")
async def remove_channel(message: Message):
    selected_channel = cursor.execute("SELECT channel_id FROM main_table WHERE user_id = ?", [message.from_user.id]).fetchone()
    if selected_channel == None:
        await message.answer("You haven't a channel")
    else:
        Methods(message.from_user.id, ..., ...).delete_channel()
        await message.answer(f"Your channel has been removed")


@router.message(F.text == "Send post")
async def send_post(message: Message, state: FSMContext):
    selected_channel = cursor.execute("SELECT channel_id FROM main_table WHERE user_id = ?",
                                      [message.from_user.id]).fetchone()
    if selected_channel == None:
        await message.answer("You haven't a channel")
    else:
        await state.set_state(Post.send_post)
        await message.answer("Send post here, please")

@router.message(Post.send_post)
async def fsm_send(message: Message, state: FSMContext):
    selected_channel = cursor.execute("SELECT channel_id FROM main_table WHERE user_id = ?", [message.from_user.id]).fetchone()[0]
    await state.update_data(post_text = message.text)
    data = await state.get_data()
    await message.copy_to(chat_id=selected_channel)
    await message.answer("Your post has been sent to your channel")
    await state.clear()