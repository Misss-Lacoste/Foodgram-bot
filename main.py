import os
import telebot
from telebot import types
import webbrowser
import json

# a='1'
# b='2'
# c='3'
# d=''
how_many_products = 0
user_products = []
# user_measure_type = []
# user_amount = []
# cou = 0

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_KEY'])

def one_product(message):
    global how_many_products
    how_many_products -= 1
    if message.text == 'стоп':
        a = user_products.copy()
        return a
    if how_many_products>=0:
        user_products.append(message.text.split(' '))
        sent = bot.send_message(message.chat.id, f'{user_products} осталось {how_many_products}')
        if how_many_products==0:
            bot.send_message(message.chat.id, f"Всё, конечный список {user_products}")
            # a = user_products.copy()
            a = {'ingrediends': user_products}
            OUR_JSON_LIST = json.dumps(a)
        else:
            bot.register_next_step_handler(sent, one_product)
    # else:
    #     sent = bot.send_message(message.chat.id, f"Всё, конечный список {user_products}")
    #     a = user_products.copy()
    # global how_many_products
    # # message_to_save = message.text
    # d=message.text
    # a,b,c = str(d).split()
    # # print('\n','\n',a,b,c,'\n','\n')
    # user_products.append(a)
    # user_measure_type.append(b)
    # user_amount.append(c)
    # how_many_products-=1
    # print(how_many_products)
    # while how_many_products > 0:
    #     t = bot.reply_to(message, f"еще {how_many_products}")
    #     how_many_products-=1
    #     bot.register_next_step_handler(t, one_product)
    #     # one_product(message)
    #     # how_many_products-=1

@bot.message_handler(commands=["site", "website"]) # пропишем декоратор для команды перехода на сайт
def site(message):
    webbrowser.open("https://espanol.online/lexic/by_theme?language=ru") #ссылка на сайт

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
    bot.send_message(message.from_user.id, text="Сколько продуктов хочешь добавить в список?", reply_markup=keyboard)
    bot.register_next_step_handler(message.text, one_product)

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_amount(callback):
    global how_many_products
    how_many_products = int(callback.data[-1])
    # bot.send_message(callback.message.chat.id, f'Напиши {callback.data[-1]} продукта(ов) in singular form in one message. Example:')
    
    bot.send_message(callback.message.chat.id, f"Выбрано {callback.data[-1]} продукта(ов)")
    s = bot.reply_to(callback.message, 'Начинай вводить название продукта, количество и единицы измерения (сколько штук, грамм '
                                                        'или миллилитров) (напиши все через пробел, пожалуйста)')
    # for i in range(int(callback.data[-1])):
    #     print('qqqqqqqqqqqqqq')
    bot.register_next_step_handler(s, one_product)
    # bot.send_message(callback.message.chat.id, f"pRoVeRkA{' '.join(user_products)}{str(user_products)}")

@bot.message_handler(commands=['start', 'hello', 'help']) #пропишем декоратор для обработки команд
def main(message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!") #обращение к id чата и id пользователя
    bot.send_photo(message.chat.id,'https://flomaster.top/uploads/posts/2022-12/1672269174_flomaster-club-p-vinni-pukh-risunok-dlya-detei-vkontakte-49.png')
    keyboard = types.InlineKeyboardMarkup() #начинаем операцию по внедрению встроенных кнопок
    key_site = types.InlineKeyboardButton(text='Website', url="https://espanol.online/lexic/by_theme?language=ru")
    keyboard.add(key_site)
    bot.send_message(message.from_user.id, text="Choose the action", reply_markup=keyboard)

@bot.message_handler(commands=['drop']) #пропишем декоратор для обработки команд
def main(message):
    global user_products
    # global user_measure_type
    # global user_amount
    bot.send_message(message.chat.id, f"Дропаю список {user_products}! Теперь он пустой!")
    user_products = []

@bot.message_handler(commands=["check"]) # пропишем декоратор для команды перехода на сайт
def check_list(message):
    global user_products
    bot.send_message(message.chat.id, f"Проверка списка: {user_products}")

@bot.message_handler(content_types=["text"]) #обработка текстового сообщения, введенного пользователем
def get_text_message(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Ку, {message.from_user.first_name}!")
        bot.send_photo(message.chat.id,
                       'https://flomaster.top/uploads/posts/2022-12/1672269174_flomaster-club-p-vinni-pukh-risunok-dlya-detei-vkontakte-49.png')
        keyboard = types.InlineKeyboardMarkup()  # начинаем операцию по внедрению встроенных кнопок
        key_site = types.InlineKeyboardButton(text='Website', url="https://espanol.online/lexic/by_theme?language=ru")
        keyboard.add(key_site)
        bot.send_message(message.from_user.id, text="Сайт", reply_markup=keyboard)

if __name__ == "__main__":
        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as e:
                print(e)