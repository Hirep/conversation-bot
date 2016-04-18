from bot import teleBotConfig
import telebot


print("Starting bot...")
bot = telebot.TeleBot(teleBotConfig.token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print("Command")
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['sticker'])
def sticker(message):
    bot.send_message(message.chat.id, "Oh, sticker")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    print("TExt message")
    print(message.text)
    bot.send_message(message.chat.id, "oh is it?")


@bot.message_handler(func=lambda m: True)
def any_msg(message):
    bot.send_message(message.chat.id, "Oh, what dfq is that")
