import requests
import telebot

def get_objects():
	return requests.get("http://localhost:3000/objects").json()

def get_object(number):
	return requests.get(f"http://localhost:3000/objects/{number}").json()

bot = telebot.TeleBot("2124560983:AAHzWFqctVTC2-Yh9hZkjx5IFWIsbw37IEA", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello")

@bot.message_handler(commands=['scp_object'])
def request_object(message):
	reply = bot.reply_to(message, "Напиши номер объекта")
	bot.register_next_step_handler(reply, find_object)

def find_object(message):
	try:
		number = int(message.text)
		object = get_object(number)
		bot.reply_to(message, object['name'])
	except Exception as e:
		bot.reply_to(message, "Что-то пошло не так :(")

bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
