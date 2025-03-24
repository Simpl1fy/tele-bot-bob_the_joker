import os
import telebot
from dotenv import load_dotenv
import requests

base_url = "https://v2.jokeapi.dev/joke/"
blacklist = "?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None);

start_text = "Hello, I am Bob, a joke bot. I can tell you jokes. You can start by command /joke."
joke_message_text = "What kind of joke do you want? Any, Programming, Misc, Dark, Pun, Spooky, Christmas. \n\nExample - Type \nany or Any \nfor any kind of joke."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Hope you are doing fine.")
    bot.send_message(message.chat.id, start_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, start_text)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

def get_new_joke(message):
    type = message.text.capitalize()
    
    if type == "Stop":
        bot.send_message(message.chat.id, "Did you not like my jokes? 😢\nIf you feel bad type /joke")
        return
    

    valid_types = ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"]
    if type not in valid_types:
        bot.send_message(message.chat.id, "Invalid type.")
        bot.send_message(message.chat.id, f"Start again by typing /joke")
        return

        
    joke = get_joke(type)
    if(joke.get('type') == 'single'):
        joke_text = f"{joke.get('joke', "Oops, I forgot the joke. Teehee")}"
    else:
        joke_text = f"{joke["setup"]} \n\n{joke["delivery"]}"
    bot.send_message(message.chat.id, "Here is your joke")
    bot.send_message(message.chat.id, joke_text)
    bot.send_message(message.chat.id, "Want another one? Type the type of joke you want. \nUse any one - Any, Programming, Misc, Dark, Pun, Spooky, Christmas.\nType stop to stop.")
    bot.register_next_step_handler(message, get_new_joke)


def get_joke(type):
    response = requests.get(f"{base_url}{type}{blacklist}")
    joke_data = response.json()
    return joke_data

@bot.message_handler(commands=['joke'])
def joke(message):
    bot.send_message(message.chat.id, joke_message_text)
    bot.register_next_step_handler(message, get_new_joke)


bot.infinity_polling()