import logging
logger = logging.getLogger(__name__)

import pyrogram
from .commands import *
from ..config import Config
from ..tools.text import TEXT
from ..plugins.rename import force_name, doc
from ..plugins.video import vid
from ..plugins.audio import aud
from pyrogram import Client as RenamerNs, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserBannedInChannel, UserNotParticipant
from pyrogram.emoji import *


################## Callback for start button ##################

@RenamerNs.on_callback_query(filters.regex('^start$'))
async def start_cb(c, m):
    await m.answer()
    await start(c, m, True)


################## Callback for help button ##################

@RenamerNs.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()
    await help(c, m, True)


################## Callback for donate button ##################

@RenamerNs.on_callback_query(filters.regex('^donate$'))
async def donate(c, m):
    button = [[
        InlineKeyboardButton(f'{HOUSE_WITH_GARDEN} Home', callback_data='back'),
        InlineKeyboardButton(f'{ROBOT} About', callback_data='about')
        ],[
        InlineKeyboardButton(f'{NO_ENTRY} Close', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await m.answer()
    await m.message.edit(
        text=TEXT.DONATE_USER.format(m.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


################## Callback for close button ##################

@RenamerNs.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


################## Callback for home button ##################

@RenamerNs.on_callback_query(filters.regex('^back$'))
async def back_cb(c, m):
    await m.answer()
    await start(c, m, True)


################## Callback for about button ##################

@RenamerNs.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    await about(c, m, True)


################## Callback for start button ##################

@RenamerNs.on_callback_query()
async def cb_handler(bot, update):
        
    if "rename_button" in update.data:
        await update.message.delete()
        await force_name(bot, update.message)
        
    elif "cancel_e" in update.data:
        await update.message.delete()
        await cancel_extract(bot, update.message)

