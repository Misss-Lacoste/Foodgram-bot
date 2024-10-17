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