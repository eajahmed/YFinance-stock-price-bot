import logging
import yfinance as yf
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = 'Your Bot Token'  # Replace with your actual bot token

def start(update, context):
    update.message.reply_text('Hi! I am a stock price bot. \nI can provide some information about stock prices. \nTo start your journey with me, please write the command. \nFor example /ticker AAPL')

def help_command(update, context):
    help_text = "Here are the available commands:\n"
    help_text += "/start - Start the bot\n"
    help_text += "/ticker <stock_symbol> - Get information about a stock\n"
    help_text += "/developer - Contact the developer\n"
    help_text += "/help - Display this help message\n\n"
    help_text += "If you don't know the specific company stock symbols or ticker command you can download the below list and use what you want."

    keyboard = [[InlineKeyboardButton("Download Stock Symbols List", callback_data='download')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(help_text, reply_markup=reply_markup)

def download_callback(update, context):
    query = update.callback_query
    query.message.reply_document(document=open('D:\BOT\Telegram Bot\StockValue\stock_symbols.csv', 'rb'))

def ticker_command(update, context):
    args = context.args

    if len(args) == 0:
        update.message.reply_text('Please provide a stock symbol. \nFor example /ticker AAPL')
        return

    try:
        details = yf.Ticker(args[0])
        info = details.info

        msg = f'\n Company Name: {info.get("longName", "Value not found")}'
        msg += f'\n Industry: {info.get("industry", "Value not found")}'
        msg += f'\n Sector: {info.get("sector", "Value not found")}'
        msg += f'\n Stock symbol: {info.get("symbol", "Value not found")}'
        msg += f'\n Market Open: {info.get("regularMarketOpen", "Value not found")}'
        msg += f'\n Market Day High: {info.get("dayHigh", "Value not found")}'
        msg += f'\n Market Day Low: {info.get("dayLow", "Value not found")}'
        msg += f'\n Market Previous Close: {info.get("previousClose", "Value not found")}'
        msg += f'\n Profit Margins: {info.get("profitMargins", "Value not found")}'
        msg += f'\n Market Volume: {info.get("volume", "Value not found")}'
        msg += f'\n Market Cap: {info.get("marketCap", "Value not found")}'
        msg += f'\n Currency: {info.get("currency", "Value not found")}'
        msg += '\n\n <i>Powered by Yahoo Finance!</i>'
        update.message.reply_text(msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except:
        update.message.reply_text('Invalid stock symbol or an error occurred.')

def error(update, context):
    logger = logging.getLogger(__name__)
    logger.error(f'Update {update} caused error {context.error}')

def developer(update, context):
    mail = "eajahmed5110@gmail.com"
    update.message.reply_text(
        f"Hello World! This Bot is Developed by EAJUDDIN AHMED. \n \nEAJUDDIN is a Front-end Web Developer and WordPress Expert. Also, he is a great Telegram Bot Developer \nContact Information: \n \nTelegram : @eajahmed \n \nLinkedin: https://www.linkedin.com/in/eajahmed \n \nMail : {mail} \n \nWhatsApp: +8801316032483"
    )

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('ticker', ticker_command))
    updater.dispatcher.add_handler(CommandHandler('developer', developer))
    updater.dispatcher.add_handler(CallbackQueryHandler(download_callback, pattern='download'))

    updater.dispatcher.add_handler(MessageHandler(Filters.update, error))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

