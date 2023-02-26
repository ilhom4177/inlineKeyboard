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

TOKEN = os.environ['TOKEN']
counter = 0  

def start(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    bot.sendMessage(chat_id=chat_id, text="Send me a Photo")

def photo(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    photo = update.message.photo[-1]["file_id"]

    button1 = InlineKeyboardButton(text="👍", callback_data="like")
    button2 = InlineKeyboardButton(text="👎", callback_data="dislike")
    keyboard = InlineKeyboardMarkup([[button1, button2]])
    bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=keyboard)

def like_and_dislike(update: Update, context: CallbackContext):
    global counter
    query = update.callback_query
    data = query.data
    
    if data == "like":
        counter += 1  
    elif data == "dislike":
        counter -= 1  
    
    query.answer()
    query.edit_message_caption(caption=f"Current count: {counter}")

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.photo, photo))
dp.add_handler(CallbackQueryHandler(like_and_dislike))
updater.start_polling()
updater.idle()