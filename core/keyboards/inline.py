from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from core.model.meeting import Meeting


def get_your_appointments(id: str):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(InlineKeyboardButton(text='בטל תור', callback_data=f'{id}'))
    keyboard_builder.adjust()
    return keyboard_builder.as_markup()



def get_name_of_service():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(InlineKeyboardButton(text='קבע פגישה', callback_data='set_meeting'))
    keyboard_builder.add(InlineKeyboardButton(text='בטל פגישה', callback_data='cancel_meeting'))
    keyboard_builder.adjust()
    return keyboard_builder.as_markup()


def get_week():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(InlineKeyboardButton(text='שבוע הבא', callback_data='שבוע הבא'))
    keyboard_builder.add(InlineKeyboardButton(text='שבוע הזה', callback_data='השבוע הזה'))
    keyboard_builder.adjust()
    return keyboard_builder.as_markup()


def get_day():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(InlineKeyboardButton(text='יום ראשון', callback_data='יום ראשון'))
    keyboard_builder.add(InlineKeyboardButton(text='יום שני', callback_data='יום שני'))
    keyboard_builder.add(InlineKeyboardButton(text='יום שלישי', callback_data='יום שלישי'))
    keyboard_builder.add(InlineKeyboardButton(text='יום רביעי', callback_data='יום רביעי'))
    keyboard_builder.add(InlineKeyboardButton(text='יום חמישי', callback_data='יום חמישי'))
    keyboard_builder.add(InlineKeyboardButton(text='יום שישי', callback_data='יום שישי'))
    keyboard_builder.adjust(2, 2)
    return keyboard_builder.as_markup()



def get_time():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(InlineKeyboardButton(text='9:00', callback_data='9:00'))
    keyboard_builder.add(InlineKeyboardButton(text='10:00', callback_data='10:00'))
    keyboard_builder.add(InlineKeyboardButton(text='11:00', callback_data='11:00'))
    keyboard_builder.add(InlineKeyboardButton(text='12:00', callback_data='12:00'))
    keyboard_builder.add(InlineKeyboardButton(text='13:00', callback_data='13:00'))
    keyboard_builder.add(InlineKeyboardButton(text='14:00', callback_data='14:00'))
    keyboard_builder.add(InlineKeyboardButton(text='15:00', callback_data='15:00'))
    keyboard_builder.add(InlineKeyboardButton(text='16:00', callback_data='16:00'))
    keyboard_builder.add(InlineKeyboardButton(text='17:00', callback_data='17:00'))
    keyboard_builder.adjust(3, 3)
    return keyboard_builder.as_markup()

    
