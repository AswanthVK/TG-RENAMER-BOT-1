import logging
logger = logging.getLogger(__name__)

import asyncio
from ..config import Config
from ..tools.text import TEXT
from ..database.database import *
from ..database.database import add_user, query_msg
from ..database.support import *
from pyrogram import Client as RenamerNs, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import PeerIdInvalid, ChannelInvalid, FloodWait, UserNotParticipant
from pyrogram.emoji import *


################## Help command ##################

@RenamerNs.on_message(filters.command("help") & filters.private & filters.incoming)
async def help(c, m, cb=False):
    button = [[
        InlineKeyboardButton(f'Updates Channel', url='https://t.me/NewBotz'),
        InlineKeyboardButton(f'Share & Support Me', url='tg://msg?text=Hai%20Friend%2C%0D%0AAm%20Introducing%20a%20Powerful%20%2A%2AConverter%20Bot%2A%2A%20for%20Free.%0D%0A%2A%2ABot%20Link%2A%2A%20%3A%20%40NewConverter_Bot')
        ],[
        InlineKeyboardButton(f'{HOUSE_WITH_GARDEN} Home', callback_data='back'),
        InlineKeyboardButton(f'{NO_ENTRY} 𝙲𝚕𝚘𝚜𝚎', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        await m.message.edit(
            text=TEXT.HELP_USER.format(m.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await m.reply_text(
            text=TEXT.HELP_USER.format(m.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )


################## start commamd ##################

@RenamerNs.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(c, m, cb=False):
    id = m.from_user.id
    user_name = '@' + m.from_user.username if m.from_user.username else None
    await add_user(id, user_name)
    owner = await c.get_users(Config.OWNER_ID)
    button = [[
        InlineKeyboardButton(f'{INFORMATION} Help', callback_data="help"),
        InlineKeyboardButton(f'{ROBOT} About', callback_data='about')
        ],[
        InlineKeyboardButton(f'{NO_ENTRY} Close', callback_data="close")
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        await m.message.edit(
            text=TEXT.START_TEXT.format(user_mention=m.from_user.mention, bot_owner=owner.mention(style="md")), 
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await m.reply_text(
            text=TEXT.START_TEXT.format(user_mention=m.from_user.mention, bot_owner=owner.mention(style="md")), 
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        ) 


@RenamerNs.on_message(filters.private & filters.command('subscribers'))
async def subscribers_count(bot, m: Message):
    id = m.from_user.id
    if id not in Config.AUTH_USERS:
        return
    msg = await m.reply_text(TEXT.WAIT_MSG)
    messages = await users_info(bot)
    active = messages[0]
    blocked = messages[1]
    await m.delete()
    await msg.edit(TEXT.USERS_LIST.format(active, blocked))


# ------------------------ Send messages to subs ----------------------------- #
@RenamerNs.on_message(filters.private & filters.command('send'))
async def send_text(bot, m: Message):
    id = m.from_user.id
    if id not in Config.AUTH_USERS:
        return
    if (" " not in m.text) and ("send" in m.text) and (m.reply_to_message is not None):
        query = await query_msg()
        for row in query:
            chat_id = int(row[0])
            try:
                await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=m.chat.id,
                    message_id=m.reply_to_message.message_id,
                    caption=m.caption,
                    reply_markup=m.reply_markup
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception:
                pass
    else:
        msg = await m.reply_text(TEXT.REPLY_ERROR, m.message_id)
        await asyncio.sleep(8)
        await msg.delete()

################## about command ##################

@RenamerNs.on_message(filters.command("about") & filters.private & filters.incoming)
async def about(c, m, cb=False):
    me = await c.get_me()
    owner = await c.get_users(Config.OWNER_ID)

    button = [[
        InlineKeyboardButton(f'{HOUSE_WITH_GARDEN} Home', callback_data='back'),
        InlineKeyboardButton(f'{NO_ENTRY} Close', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        await m.message.edit(
            text=TEXT.ABOUT,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await m.reply_text(
            text=TEXT.ABOUT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )


################## Mode command ##################

@RenamerNs.on_message(filters.command("mode") & filters.private & filters.incoming)
async def set_mode(c, m):
    upload_mode = (await get_data(m.from_user.id)).upload_mode
    if upload_mode:
        await update_mode(m.from_user.id, False)
        text = f"From Now all files will be **Uploaded as Video** {VIDEO_CAMERA}"
    else:
        await update_mode(m.from_user.id, True)
        text = f"From Now all files will be **Uploaded as Files** {FILE_FOLDER}"
    await m.reply_text(text, quote=True)
    

################## reset command ##################

@RenamerNs.on_message(filters.command("reset") & filters.private & filters.incoming)
async def reset_user(c, m):
    if m.from_user.id in Config.AUTH_USERS:
        if len(m.command) == 2:
            cmd, user_id = m.command
            try:
                status = await del_user(user_id)
            except Exception as e:
                logger.error(e)
                return await m.reply_text(f'__Error while deleting user from Database__\n\n**Error:** `{e}`')
            if status:
                await m.reply_text(f"Sucessfully removed user with id {user_id} from database")
            else:
                await m.reply_text('User not exist in Database')
        else:
            await m.reply_text('Use this command in the format `/reset user_id`')
    else:
        await m.reply_sticker(sticker="CAACAgIAAx0CVjDmEQACS3lgvEO2HpojwIQe8lqa4L66qEnDzQACjAEAAhZCawq6dimcpGB-fx8E", quote=True)
        await m.reply_text(text="You are not admin to use this command.")


################## login command ##################

@RenamerNs.on_message(filters.command('login') & filters.incoming & filters.private)
async def password(c, m):
    if Config.BOT_PASSWORD:
        if Config.AUTH_USERS is None:
            Config.AUTH_USERS = [Config.OWNER_ID]
        if m.from_user.id in Config.AUTH_USERS:
            return await m.reply_text(f"__Hey you are auth user of this bot so you don't want to login {DETECTIVE_LIGHT_SKIN_TONE}.__")

        is_logged = (await get_data(m.from_user.id)).is_logged
        if is_logged:
            return await m.reply_text(f"__You are already loggedin {VICTORY_HAND}.__", quote=True)

        if len(m.command) == 1:
            await m.reply_text('Send me the bot password in the format `/login password`')
        else:
            cmd, pwd = m.text.split(' ', 1)
            if pwd == Config.BOT_PASSWORD:
                await update_login(m.from_user.id, True)
                await m.reply_text(text=LOCKED_WITH_KEY, quote=True)
                await m.reply_text(f'Logged Sucessfully to the bot.\nEnjoy the bot now {FACE_SAVORING_FOOD}.', quote=True)
            else:
                await m.reply_sticker(sticker="CAACAgQAAxkBAAIlHWC8WTwz55v_w0laDRuSrwL2oWRTAALtDAACYLUpUtRT8sziJp59HwQ", quote=True)
                return await m.reply_text(f'Incorrect password', quote=True)
    else:
        await m.reply_text(f'**This bot was publicly available to all {SMILING_FACE_WITH_HEARTS}.**\nIf you are the owner of the bot to make bot private add bot password in Config Vars {LOCKED_WITH_KEY}.', quote=True)


