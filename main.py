import os
import json
import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_KEY'])

dishes_from_DB = 0
def dishes_output(message): #вывод блюд
    for i in dishes_from_DB['response']['items']:
        bot.send_message(message.chat.id, f"{i['name']}")
        bot.send_message(message.chat.id, f"{i['recipe']}")

@bot.message_handler(commands=["site", "website"]) # пропишем декоратор для команды перехода на сайт
def site(message):
    webbrowser.open("https://bla-bla-bla") #ссылка на сайт

@bot.message_handler(commands=['start', 'hello', 'help']) #пропишем декоратор для обработки команд
def main(message):
    bot.send_message(message.chat.id, f"Приветик, {message.from_user.first_name}! Я - шеф-бот, который с радостью поможет тебе найти вкусный рецепт! Вперёд, к рецептам!") #обращение к id чата и id пользователя
    bot.send_photo(message.chat.id,'https://alumni.hse.ru/mirror/pubs/share/368986685')
    keyboard = types.InlineKeyboardMarkup() #начинаем операцию по внедрению встроенных кнопок
    key_site = types.InlineKeyboardButton(text='Перейти на веб-сайт', url="bla-bla-bla")
    keyboard.add(key_site)
    key_food = types.InlineKeyboardButton(text='Вписать ингредиенты', callback_data='food_btn')
    keyboard.add(key_food)
    bot.send_message(message.from_user.id, text="Выберите действие", reply_markup=keyboard)


@bot.message_handler(content_types=["text"]) #обработка текстового сообщения, введенного пользователем
def get_text_message(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Приветик, {message.from_user.first_name}! Я - шеф-бот, который с радостью поможет тебе найти вкусный рецепт! Вперёд, к рецептам!")
        bot.send_photo(message.chat.id,
                       'https://alumni.hse.ru/mirror/pubs/share/368986685')
        keyboard = types.InlineKeyboardMarkup()  # начинаем операцию по внедрению встроенных кнопок
        key_site = types.InlineKeyboardButton(text='Перейти на веб-сайт', url="https://espanol.online/lexic/by_theme?language=ru")
        key_food = types.InlineKeyboardButton(text='Вписать ингредиенты', callback_data='food_btn')
        keyboard.add(key_food)
        keyboard.add(key_site)
        bot.send_message(message.from_user.id, text="Выберите действие", reply_markup=keyboard)
    elif message.text.lower() == "очистить":
        ingrediends = []
    elif message.text.lower() == "рецепт":
        bot.send_message(message.chat.id, text='Введите ингредиенты через запятую (например, яйца, молоко, соль)')
        sent = bot.send_message(message.chat.id, text='Как закончите, напишите "стоп"')
        bot.register_next_step_handler(sent, func_recipe)
    else:
        bot.send_message(message.chat.id, text='Я не понимаю ваш запрос. Попробуйте снова.')
    

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'food_btn':
        bot.send_message(callback.message.chat.id, text='Напишите название продукта')
        sent = bot.send_message(callback.message.chat.id, text='Как закончите, напишите стоп')
        bot.register_next_step_handler(sent, func_food)

ingrediends = []
@bot.message_handler(content_types=['food'])
def func_food(message):
    if message.text.lower() == 'стоп':
        a = {'ingrediends': ingrediends[:]}
        OUR_JSON_LIST = json.dumps(a).encode('utf8').decode()
        dishes_from_DB = json.loads() #сюда файл из базы данных, нужно допилить
        dishes_output(message) #вывод блюд
        ingrediends.clear()
        print(a)
        return
    ingrediends.append(message.text)
    sent = bot.send_message(message.chat.id, text='Что-нибудь еще?')
    bot.register_next_step_handler(sent, func_food)

ingrediends = []
def find_recipe(ingredients):#Ищет рецепты по заданным ингредиентам
    #возвращает Список рецептов, содержащих все указанные ингредиенты
    with open('recipes.json', 'r') as f:
        data = json.load(f)
    matching_recipes = []
    for recipe in data["recipes"]:  
        if all(ingredient in recipe["ingredients"] for ingredient in ingredients):
          matching_recipes.append(recipe)
    return matching_recipes

@bot.message_handler(content_types=['text'])
def func_recipe(message):
  if message.text.lower() == 'стоп':
    ingredients = [ingr.strip().lower() 
for ingr in message.text.split(",")] # Очистка ввода
    recipes = find_recipe(ingredients) # Поиск рецептов
    if recipes:
      for recipe in recipes:
        bot.send_message(message.chat.id, f"Рецепт: {recipe['name']}")
        bot.send_message(message.chat.id, f"Ингредиенты: {', '.join(recipe['ingredients'])}")
        bot.send_message(message.chat.id, f"Инструкции: {recipe['instructions']}")
    else:
      bot.send_message(message.chat.id, text='Я не нашел рецептов с такими ингредиентами. Попробуйте снова.')
    ingrediends.clear()
    return

  ingrediends.append(message.text)
  sent = bot.send_message(message.chat.id, text='Введите еще один ингредиент или напишите "стоп".')
  bot.register_next_step_handler(sent, func_recipe)



if __name__ == "__main__":
        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as e:
                print(e)