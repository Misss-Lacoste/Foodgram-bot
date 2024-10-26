import os
import json
import telebot
from telebot import types
import webbrowser
import requests

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_KEY'])

dishes_from_DB = []
def dishes_output(message, dishes_from_DB): #вывод блюд
    for i in dishes_from_DB:
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
        # a = {'ingrediends': ingrediends[:]}
        # OUR_JSON_LIST = json.dumps(a).encode('utf8').decode()
        #dishes_from_DB = json.loads(requests.request(method='get', url='http://127.0.0.1:8000/api/recipy', data=a).json())
        # dishes_from_DB = json.load(open("C:\egeinf\eee.json"))
        dishes_from_DB = [{"name": "Щи", "recipe": "1. Мясо промываем, кладем в кастрюлю, заливаем холодной водой и доводим до кипения, периодически снимая с поверхности шум. Затем уменьшаем огонь и варим в течение часа. Мясо вынимаем, нарезаем ипериодически снимая с поверхности шум. Затем уменьшаем огонь и варим в течение часа. Мясо вынимаем, нарезаем ивозвращаем обратно.\n2.Лук и морковь очищаем. Лук режем мелко, а морковь трем на терке.\n3. На раскаленной сковородеподогреваем небольшое количество растительного масла и обжариваем на нем лук до мягкости. Добавляем морковь и томатнуюпасту и тушим все вместе 5-7 минут.\n4. Картофель очищаем, нарезаем кубиком, капусту шинкуем и добавляем овощи в бульон.Еще раз доводим до кипения.\n5. Добавляем в суп зажарку и варим 20 минут, затем соль растираем с чесноком, добавляем всуп, перчим, добавляем лавровый лист. Зелень мелко рубим.\n6. Даем настояться в течение 10 минут под крышкой.", "time":"1:00:00"}, {"name": "Борщ", "recipe": "1. Положите в кастрюлю мясо, залейте водой и поставьте на плиту вариться. Послезакипания убавьте огонь до минимума.\n2. Нашинкуйте капусту и нарежьте кубиками или соломкой картошку и добавьте.\n3.Натрите на крупной терке или нарежьте тоненькой соломкой морковь и свеклу.\n4. Поставьте сковороду нагреваться насредний огонь, влейте в нее растительное масло. Когда она станет горячей, выложите свеклу и морковь.\n5.Перемешайтеовощи и добавьте к ним лук.\n6. Обжаривайте овощи, пока они не станут мягкими и примерно однородного цвета. Не забывайтерегулярно перемешивать.", "time": "1:20:00"}, {"name": "Картошка жареная", "recipe": "1. Гречневую крупу перебрать ихорошо промыть. Вскипятить воду.\n2. Добавить крупу и соль.\n3. Уменьшить огонь, накрыть крышкой и варить гречку 20минут.", "time": "0:30:00"}]
        bot.send_message(message.chat.id, text=f"{str(ingrediends)}")
        dishes_output(message, dishes_from_DB) #вывод блюд
        ingrediends.clear()
        # print(a)
        return
    ingrediends.append(message.text)
    bot.send_message(message.chat.id, text=f"{str(ingrediends)}")
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
                print("POLLING",e)