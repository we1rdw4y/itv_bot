import os
import sys

import telebot

TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('BOT_ADMIN')
if not TOKEN:
    print("token empty")
    sys.exit('token empty')
if not ADMIN:
    print("admin empty")
    sys.exit('admin empty')

bot = telebot.TeleBot(TOKEN, parse_mode=None)

states = dict()
# Key = UserID, value = data

def main():
    print('starting polling')
    bot.infinity_polling()

@bot.message_handler(commands=['me'])
def me(msg):
    bot.reply_to(msg, msg.from_user)

@bot.message_handler(commands=['chat'])
def chat(msg):
    bot.reply_to(msg, msg.chat)

@bot.message_handler(commands=['start', 'help'])
def send_message(msg):
    bot.send_message(msg.chat.id, "Введите описание эвента")

@bot.message_handler(content_types=['text', 'photo'], func=lambda msg: True)
def process(msg):
    if msg.from_user.id not in states:
        states[msg.from_user.id] = msg.text
        bot.send_message(msg.chat.id, "Приложите картинку для афиши")
        return
    if not msg.photo:
        bot.reply_to(msg, "Photo is empty")
        return
    photo_width_max = 0
    photo_id = ''
    for photo in msg.photo:
        if photo.width <= photo_width_max:
            continue
        photo_width_max = photo.width
        photo_id = photo.file_id
    bot.send_photo(chatid, photo_id, caption=states[msg.from_user.id])
    del states[msg.from_user.id]
    bot.send_message(msg.chat.id, "Заявка принята")

if __name__ == "__main__":
    main()
