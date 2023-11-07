from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from core.model.meeting import Meeting
from core.utils.dbconnect import Request
from core.utils.commands import set_commands
from core.keyboards.inline import get_day, get_name_of_service, get_week, get_time, get_your_appointments
from core.middleware.settings import settings
from core.utils.dbconnect import Request
from core.utils.state import State


form_router = Router()
appointment = Meeting()
list_of_meetings: [Meeting] = []


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(State.initial)
    await message.answer('אנא בחר מהאפשרויות הבאות', reply_markup=get_name_of_service())
    await state.set_state(State.set_name)
    await state.update_data(user_id=message.from_user.id)


@form_router.callback_query(State.set_name)
async def set_name(call: CallbackQuery, state: FSMContext, request: Request) -> None:
    print(f'DATA IN SET_NAME-> {call.data}')
    if call.data == 'set_meeting':
        await call.message.answer('מתי אתה מעדיף לקבוע את התור שלך', reply_markup=get_week())
        await state.set_state(State.set_week)
    elif call.data == 'cancel_meeting':
        # SHOULD BE IMPLEMENTED LATER - CANCEL MEETING FUNCTION
        await show_meetings(call, state, request)
        if list_of_meetings is not None:
            await call.message.answer('בחר פגישה לביטול')
            for meeting in list_of_meetings:
                print(f'Meeting: {meeting.name} - {meeting.id}')
                name = meeting.name
                week = meeting.week
                day = meeting.day
                time = meeting.time
                id = meeting.id
                await call.message.answer(f'{name} \n{week}, {day}, {time}', reply_markup=get_your_appointments(id=id))
            await state.set_state(State.cancel_me)
        else:
            await call.message.answer('אין לך פגישות קבועות')
            state.set_state(State.initial)



@form_router.callback_query(State.cancel_me)  
async def cancel_me(call: CallbackQuery, state: FSMContext, request: Request) -> None:
    print(f'DATA IN CANCEL_ME-> {int(call.data)}')
    print(f'TYPE OF CALL DATA -> {type(call.data)}')
    id = int(call.data)
    print(f'TYPE OF ID -> {type(id)}')
    await delete_meeting(id=id, state=state, request=request, call=call)



@form_router.callback_query(State.set_week)
async def set_week(call: CallbackQuery, state: FSMContext) -> None:
    print(f'DATA IN SET_WEEK-> {call.data}')
    # SHOULD BE IMPLEMENTED LATER - GET WEEK FUNCTION
    await call.message.answer('בחר יום', reply_markup=get_day())
    await state.set_state(State.set_day)
    await state.update_data(week = call.data)


@form_router.callback_query(State.set_day)
async def set_day(call: CallbackQuery, state: FSMContext) -> None:
    print(f'DATA IN SET_DAY-> {call.data}')
    # SHOULD BE IMPLEMENTED LATER - GET DAY FUNCTION
    await call.message.answer('בחר שעה', reply_markup=get_time())
    await state.set_state(State.set_time)
    await state.update_data(day = call.data)



@form_router.callback_query(State.set_time)
async def set_time(call: CallbackQuery, state: FSMContext, request: Request) -> None:
    print(f'DATA IN SET_TIME-> {call.data}')
    await state.set_state(State.set_confirm)
    await state.update_data(time = call.data)
    # print(f'DATA -> {await state.get_data()}')
    # print(f'STATE -> {await state.get_state()}')
    await confirm_meeting(call, state, request)


async def confirm_meeting(call: CallbackQuery, state: FSMContext, request: Request) -> None:
    data = await state.get_data()
    week = data.get('week')
    day = data.get('day')
    time = data.get('time')
    user_id = data.get('user_id')

    try:
        await request.create_meeting(name='meeting', week=week, day=day, time=time, user_id=user_id)
        await call.message.answer(f'הפגישה נקבעה:\n{time}, {day}, {week}')
        await state.set_state(State.initial)
        list_of_meetings.clear()
        await state.clear()
        print(f'DATA CLEARED -> {await state.get_data()}')
    except Exception as e:
        print(f'Exception during sending message: {e}')


async def show_meetings(call: CallbackQuery, state: FSMContext, request: Request) -> None:
    data = await state.get_data()
    user_id = data.get('user_id')

    try:
        meetings = await request.get_meetings(user_id=user_id)
        # for meeting in meetings:
        #     print(f'Meeting: {meeting.get("name")} - {meeting.get("id")}')
        
        list_of_meetings.clear()  # Clear the list before populating it again

        for meeting in meetings:
            new_appointment = Meeting()  # Create a new instance for each meeting
            new_appointment.set_name(meeting.get('name'))
            new_appointment.set_week(meeting.get('week'))
            new_appointment.set_day(meeting.get('day'))
            new_appointment.set_time(meeting.get('time'))
            new_appointment.set_id(str(meeting.get('id')))
            new_appointment.set_user_id(meeting.get('user_id'))
            list_of_meetings.append(new_appointment)

        for meeting in list_of_meetings:
            meeting.print_meeting() 

    except Exception as e:
        print(f'Exception during getting meetings: {e}')


async def delete_meeting(id: int, state: FSMContext, request: Request, call: CallbackQuery) -> None:
    try:
        await request.delete_meeting(id=id)
        await state.set_state(State.initial)
        await state.clear()
        print(f'DATA CLEARED -> {await state.get_data()}')
        await call.message.answer('!הפגישה בוטלה בהצלחה')
    except Exception as e:
        print(f'Exception during deleting meeting: {e}')

             

