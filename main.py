import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

def get_objects():
	return requests.get(f"{os.getenv('API_URL')}/objects").json()

def get_object(number):
	return requests.get(f"{os.getenv('API_URL')}/objects/{int(number)}").json()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello")

@bot.message_handler(commands=['scp_object'])
def request_object(message):
	reply = bot.reply_to(message, "Напиши номер объекта")
	bot.register_next_step_handler(reply, reply_with_object)

def reply_with_object(message):
	try:
		object = get_object(message.text)
		bot.reply_to(message, object['name'])
	except Exception as e:
		bot.reply_to(message, "Что-то пошло не так :(")		

bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
