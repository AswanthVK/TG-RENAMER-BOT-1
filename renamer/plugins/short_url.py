'''
© All rights reserved by Mrvishal2k2

Kangers dont f*ckin kang this !!!
Should have to give credits 😏 else f***off 
This is only for personal use Dont use this for ur bot channel business 😂
Thanks to Mahesh Malekar for his Gplinks Bot !!
'''

# Bitly Bot

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from pyshorteners import Shortener
from renamer.config import Config


@Client.on_message(filters.regex(r'https?://[^\s]+'))
#@Client.on_message(filters.command(["shorturl"]))
async def link_handler(bot, update):
    file_name = None
    url = update.text
    #log_msg = None
    #log_msg = await update.forward(chat_id=BIN_CHANNEL)
    #if update.reply_to_message is not None:
        #reply_message = update.reply_to_message
    link = update.matches[0].group(0)
    shortened_url, Err = get_shortlink(link)
    if shortened_url is None:
        message = f"Something went wrong \n{Err}"
        #await log_msg.reply_text(f'**User Name:** {update.from_user.mention(style="md")}\n\n**User Id:** `{update.from_user.id}`\n\n**Shortened Link :** Failed\n\nCheck logs for error')
        await update.reply(message, quote=True)
        return
    message = f"**URL:** {url}\n\nHere is your shortlink\n`{shortened_url}`"
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Link 🔗", url=shortened_url)]])
    # i don't think this bot with get sending message error so no need of exceptions
    #await log_msg.reply_text(text=f"**User Name :** [{update.from_user.first_name}](tg://user?id={update.from_user.id})\n\n**User Id :** `{update.from_user.id}`\n\n**Shortened Link :** {shortened_url}", disable_web_page_preview=True, parse_mode="Markdown", quote=True)
    await update.reply_text(text=message, reply_markup=markup, quote=True)
      
def get_shortlink(url):
    shortened_url = None
    Err = None
    try:
       if Config.BITLY_KEY:
           ''' Bittly Shorten'''
           s = Shortener(Config.BITLY_KEY)
           shortened_url = s.bitly.short(url)
       #else:
           #''' Da.gd : I prefer this '''
           #s = Shortener()
           #shortened_url = s.dagd.short(url)
    except Exception as error:
        Err = f"#ERROR: {error}"
        log.info(Err)
    return shortened_url,Err
        
        
