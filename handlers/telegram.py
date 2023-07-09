import telebot
bot_token = "Input here token from BotFather"
chat_id = "Input here your id from IdBot"
def send_notify(message):
    bot = telebot.TeleBot(bot_token)
    bot.send_message(chat_id, message)
    