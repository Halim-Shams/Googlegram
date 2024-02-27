import requests as re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
BOT_USERNAME = '@googlgram_bot'

# Searches the google if ther is a hilight for it
def searcher(q: str):    
    response = re.get(f'https://www.google.com/search?q={q}')
    soup = BeautifulSoup(response.text, 'html.parser')
    span = soup.find_all('span')[9]
    hilights = span.parent
    hilighted_spans = hilights.find_all('span')
    hilighted_response = ''
    for span in hilighted_spans:
        try:  
            hilighted_response += span.string
        except:
            return "Couldn't found a proper hilight :()"

    if len(hilighted_response) > 0:
        return hilighted_response
    else:
        return "Couldn't found a proper hilight :()"
    
# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action='typing')
    await update.message.reply_text(f'Hey dear {update.effective_user.first_name}! What do you want to google? Just send it to me to hand you back the best result possible.')
    print(update.effective_chat.first_name)
    
# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action='typing')
    help_info = '''
    /start - Start the bot.
    /help - How to use the bot.
    
    This bot is trained on the Google search results, unlike Google that piles up all the websites and stuff, it will hand you back what you want in an instance.
    
    No more tedious explorations!
    '''
    await update.message.reply_text(help_info)
    
    
# Reply handler
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    
    if chat_type == 'supergroup':
        group_message = update.message.text
        if BOT_USERNAME in group_message:
            if update.message.text:
                await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action='typing')
                queue = update.message.text
                new_queue = queue.replace(BOT_USERNAME, '').strip()
                result = searcher(new_queue)
                await update.message.reply_text(result, reply_to_message_id=update.message.message_id)
            else:
                await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action='typing')
                await update.message.reply_text('Send me text, photos and files are not supported yet.')
    
    else:
        if update.message.text:
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action='typing')
            queue = update.message.text
            result = searcher(queue)
            await update.message.reply_text(result, reply_to_message_id=update.message.message_id)
        else:
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action='typing')
            await update.message.reply_text('Send me text, photos and files are not supported yet.')
        


if __name__ == '__main__':
    print('Starting bot...')
    app = ApplicationBuilder().token(API_TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.ALL, reply_handler))
    print('Polling...')
    app.run_polling()