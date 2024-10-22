import os
import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_KEY'])

@bot.message_handler(commands=["site", "website"]) # пропишем декоратор для команды перехода на сайт
def site(message):
    webbrowser.open("https://espanol.online/lexic/by_theme?language=ru") #ссылка на сайт

@bot.message_handler(commands=['start', 'hello', 'help']) #пропишем декоратор для обработки команд
def main(message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!") #обращение к id чата и id пользователя
    bot.send_photo(message.chat.id,'https://flomaster.top/uploads/posts/2022-12/1672269174_flomaster-club-p-vinni-pukh-risunok-dlya-detei-vkontakte-49.png')
    keyboard = types.InlineKeyboardMarkup() #начинаем операцию по внедрению встроенных кнопок
    key_site = types.InlineKeyboardButton(text='Website', url="https://espanol.online/lexic/by_theme?language=ru")
    keyboard.add(key_site)
    bot.send_message(message.from_user.id, text="Choose the action", reply_markup=keyboard)

@bot.message_handler(commands=['products'])
def products(message):
    keyboard = types.InlineKeyboardMarkup()
    p1 = types.InlineKeyboardButton(text='1',callback_data='b1')
    p2 = types.InlineKeyboardButton(text='2',callback_data='b2')
    p3 = types.InlineKeyboardButton(text='3',callback_data='b3')
    p4 = types.InlineKeyboardButton(text='4',callback_data='b4')
    p5 = types.InlineKeyboardButton(text='5',callback_data='b5')
    p6 = types.InlineKeyboardButton(text='6',callback_data='b6')
    p7 = types.InlineKeyboardButton(text='7',callback_data='b7')
    p8 = types.InlineKeyboardButton(text='8',callback_data='b8')
    p9 = types.InlineKeyboardButton(text='9',callback_data='b9')
    keyboard.add(p1,p2,p3,p4,p5,p6,p7,p8,p9)
    bot.send_message(message.from_user.id, text="How many products you have?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_amount(callback):
    bot.send_message(callback.message.chat.id, f'Write {callback.data[-1]} product(s) in singular form in one message. Example:')
    bot.send_message(callback.message.chat.id, 'egg butter flour')

@bot.message_handler(content_types=["text"]) #обработка текстового сообщения, введенного пользователем
def get_text_message(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!")
        bot.send_photo(message.chat.id,
                       'https://flomaster.top/uploads/posts/2022-12/1672269174_flomaster-club-p-vinni-pukh-risunok-dlya-detei-vkontakte-49.png')
        keyboard = types.InlineKeyboardMarkup()  # начинаем операцию по внедрению встроенных кнопок
        key_site = types.InlineKeyboardButton(text='Website', url="https://espanol.online/lexic/by_theme?language=ru")
        keyboard.add(key_site)
        bot.send_message(message.from_user.id, text="Choose the action", reply_markup=keyboard)

if __name__ == "__main__":
        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as e:
                print(e)