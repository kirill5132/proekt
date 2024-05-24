from telegram import Bot, Update
from telegram import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup


TOKEN = '6961538103:AAHAEnYPauTwon9Bh4yWCuwA5rR4ewxQIlw'


def start(update, context):
    update.message.reply_text('Привет! Я могу парсить сайты для тебя.')


def help(update, context):
    update.message.reply_text('Чтобы начать, просто отправьте мне URL сайта.')


def parse_site(update, context):
    url = 'http://example.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').text
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        print(paragraph.text)


    update.message.reply_text('Сайт успешно отпарсен.')


def error_handler(update, context):
    print(f'Update {update} caused error {context.error}')


updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('help', help))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, parse_site))
dp.add_error_handler(error_handler)

updater.start_polling()
updater.idle()