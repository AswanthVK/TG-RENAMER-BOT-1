import logging
logger = logging.getLogger(__name__)

from ..config import Config
from ..tools.text import TEXT
from ..tools.progress_bar import humanbytes
from ..database.database import *
from pyrogram import Client as RenamerNs, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
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


@RenamerNs.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.voice | filters.video_note))   
async def rename_cb(bot, update):
 
    file = update.document or update.video or update.audio or update.voice or update.video_note
    try:
        filename = file.file_name
    except:
        filename = "Not Available"  

    else:
        filesize = file.file_size
        filetype = file.mime_type
        types = file.mime_type.split("/")
        mime = types[0]

    #if Config.TIME_GAP:
        #time_gap = await timegap_check(update)
        #if time_gap:
            #return
 
    #if Config.BANNED_USERS:
        #if update.from_user.id in Config.BANNED_USERS:
            #return await update.reply_text(f'Sorry!, You are BANNED.', quote=True)
 
    #if update.from_user.id not in Config.BANNED_USERS:
        #update_channel = Config.UPDATE_CHANNEL
    #if update_channel:
        #try:
            #user = await bot.get_chat_member(update_channel, update.chat.id)
            #if user.status == "kicked":
               #await update.reply_text(" Sorry, You are **B A N N E D**")
               #return
        #except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            #await update.reply_text(
                #text="**Please Join My Update Channel Before Using Me..**",
                #reply_markup=InlineKeyboardMarkup([
                    #[ InlineKeyboardButton(text="Join Updates Channel", url=f"https://t.me/{update_channel}")]
              #])
            #)
            #return
        #else:
    if mime == "video":
            markup = InlineKeyboardMarkup([[ 
            InlineKeyboardButton("📁 Documents",callback_data = "doc"), 
            InlineKeyboardButton("🎥 Video",callback_data = "vid") ]])
    elif mime == "audio":
            markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Documents",callback_data = "doc")
            ,InlineKeyboardButton("🎵 audio",callback_data = "aud") ]])
    else:
            markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Documents",callback_data = "doc") ]]) 		
        		       
    await bot.send_message(
        chat_id=update.chat.id,
        text="<b>File Name:</b> <code>{}</code> \n<b>Size:</b> {} \n<b>Format:</b> {} ".format(filename,humanbytes(filesize),filetype),
        reply_markup=markup,
        #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Rename", callback_data="rename_button"),
                                                #InlineKeyboardButton(text="Cancel", callback_data="cancel_e")]]),
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True   
    )   
