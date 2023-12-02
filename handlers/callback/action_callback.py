from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from db.read_db import get_all_manhva_names, get_user_manhva_names
from states.user_states import UserActionState
from keyboards.back_button import back_button
from keyboards.inline_user_action import user_actions

router = Router()


@router.callback_query(F.data == 'new')
async def new_manhva_callback(callback: CallbackQuery, state: FSMContext):
	await callback.message.delete()
	await callback.message.answer('Введите манхвы которые хотите добавить(через // например манхва1//манхва2//манхва3).'
								  , reply_markup=back_button())
	await state.set_state(state=UserActionState.add_manhva)


@router.callback_query(F.data == 'remove')
async def new_manhva_callback(callback: CallbackQuery, state: FSMContext):
	await callback.message.delete()
	await callback.message.answer('Введите название манхвы которую хотите удалить.', reply_markup=back_button())
	await state.set_state(state=UserActionState.remove_manhva)


@router.callback_query(F.data == 'arch')
async def new_manhva_callback(callback: CallbackQuery, state: FSMContext):
	await callback.message.delete()
	await callback.message.answer('Введите название манхвы которую хотите архивировать.', reply_markup=back_button())
	await state.set_state(state=UserActionState.archive_manhva)


@router.callback_query(F.data == 'check')
async def new_manhva_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
	await callback.message.delete()
	all_manhva_names = await get_user_manhva_names(session=session, user_id=callback.from_user.id)
	text = ''
	for i, name in enumerate(all_manhva_names):
		text += f'{i+1}) {name}\n'
	await callback.message.answer(text=f'Ваш список отслеживания\n{text}', reply_markup=user_actions())
	await state.set_state(state=None)


@router.callback_query(F.data == 'back')
async def back_callback(callback: CallbackQuery):
	await callback.message.delete()
	await callback.message.answer('Выберите действие', reply_markup=user_actions())
