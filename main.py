
import telebot
import requests
from bs4 import BeautifulSoup
from typing import Optional

TOKEN = '6961538103:AAHAEnYPauTwon9Bh4yWCuwA5rR4ewxQIlw'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я могу парсить сайты для тебя. Прежде чем приступить отправь мне сайт "
                                      "в виде https://example.com")

@bot.message_handler(commands=['help'])
def helping(message):
    bot.send_message(message.chat.id, "Чтобы начать, просто отправьте мне URL сайта.")

@bot.message_handler(content_types=['text'])
def parse_site(message):
    url = message.text
    if not url.startswith('http'):
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте URL в формате https://example.com')
        return
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').text
        script = soup.find('script').text
        paragraphs = soup.find_all('p')
        parsed_text = f"Заголовок: {title}\n\n"
        for paragraph in paragraphs:
            parsed_text += f"{paragraph.text}\n\n"
        parsed_text = f"Заголовок: {script}\n\n"
        for paragraph in paragraphs:
            parsed_text += f"{paragraph.text}\n\n"
        bot.send_message(message.chat.id, parsed_text)
        bot.send_message(message.chat.id, 'Сайт успешно отпарсен!')
    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка при парсинге сайта: {}'.format(e))

bot.infinity_polling()
