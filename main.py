from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, 
    Dispatcher, 
    CallbackContext, 
    Filters, 
    MessageHandler, 
    CommandHandler, 
    CallbackQueryHandler)
import os

TOKEN=os.environ['TOKEN']

def start(update: Update, context: CallbackContext):
    bot = context.bot
    
    chat_id = update.message.chat.id
    text = update.message.text
    bot.sendMessage(chat_id=chat_id, text="Send me a Photo")

def photo(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    photo = update.message.photo[-1]["file_id"]

    button1 = InlineKeyboardButton(text = "👍", callback_data="like")
    button2 = InlineKeyboardButton(text = "👎", callback_data="dislike")

    keyboard = InlineKeyboardMarkup([[button1, button2]])
    bot.sendPhoto(chat_id=chat_id, photo=photo, reply_markup=keyboard)

def like_and_dislike(update: Update, context: CallbackContext):
    query = update.callback_query
    print(query.data)

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.photo, photo))
dp.add_handler(CallbackQueryHandler(like_and_dislike))
updater.start_polling()
updater.idle()