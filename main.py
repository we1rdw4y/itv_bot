import os

import telebot

bot = None

def main():
    global bot
    print('bot started')
    token = os.getenv('BOT_TOKEN')
    if not token:
        print('token error')
        return
    bot = telebot.TeleBot(token, parse_mode=None)
    bot.message_handler(commands=['start', 'help'])(send_message)
    bot.message_handler(commands=['me'])(me)
    bot.message_handler(func=lambda msg: True)(forward)
    print('starting polling')
    bot.infinity_polling()

def me(msg):
    bot.reply_to(msg, msg.from_user)

def send_message(msg):
    bot.reply_to(msg, "Howdy, how are you doing?")

def forward(msg):
    chatid = os.getenv('BOT_ADMIN')
    if not chatid:
        bot.reply_to(msg, 'admin id not found')
        return
    # print('chat id:', chatid)
    text = f'from: {msg.from_user.username}\n'
    text += msg.text
    bot.send_message(chatid, text)

if __name__ == "__main__":
    main()
