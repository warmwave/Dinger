import os
import sqlite3
import telebot
import time
import random
from telebot import types
import urllib.request as urllib

import requests.exceptions as r_exceptions
from requests import ConnectionError

import const, base, markups, temp, config

bot = telebot.TeleBot(const.token)
uploaded_items = {}


# Обработка /start команды - ветвление пользователей на покупателя и продавца
@bot.message_handler(commands=['start'])
def start(message):
    base.add_user(message)
    if base.is_seller(message.from_user.id):
        bot.send_message(message.chat.id, const.welcome_celler, reply_markup=markups.start())
    else:
        bot.send_message(message.chat.id, const.welcome_client, reply_markup=markups.start1())


# Выдача меню с типами товаров
@bot.message_handler(regexp='Меню')
def client_panel(message):
    bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=markups.show_types(message.chat.id))


@bot.callback_query_handler(func=lambda call: call.data == 'client_panel')
def client_panel(call):
    bot.edit_message_text(const.welcome_client, chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id, text='...', reply_markup=markups.start1())

# Запуск обработчика продавцов
@bot.callback_query_handler(func=lambda call: call.data == 'celler_panel')
def celler_panel(call):
    bot.edit_message_text('Админка. Выбери действие.', call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown', reply_markup=markups.edit())


# Переход в категории
def hello(message):
    if message.text != 'Сделать заказ' and message.text != 'Отзывы' and message.text != 'Поддержка' and message.text != 'Стать продавцом' and message.text != 'Как работает':
        a = random.randint(50, 100)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('Органика', 'Синтетика')
        keyboard.row('Прочее', 'Назад')
        bot.send_message(message.chat.id,
                             'В городе {name} найдено '.format(name=message.text) + str(a) + ' результатов.')
        print(message.text)
        bot.send_message(message.chat.id, 'Выберите нужную категорию.', reply_markup=markups.show_types(message.chat.id))


# Отображение товаров и занесение их в кэш
@bot.callback_query_handler(func=lambda call: call.data in base.give_menu())
def show_items(call):
    for item in base.type_finder(call.data):
        key = item.get_desc2()
        uploaded_items[str(item.id)] = 0
        print(uploaded_items)
        try:
            url = item.url
            photo = open("temp.jpg", 'w')  # Инициализация файла
            photo.close()
            photo = open("temp.jpg", 'rb')
            urllib.urlretrieve(url, "temp.jpg")
            bot.send_photo(chat_id=call.message.chat.id, photo=photo)
            bot.send_message(call.message.chat.id, item.description, reply_markup=key)
            photo.close()
            os.remove("temp.jpg")
        except Exception:
                bot.send_message(call.message.chat.id, item.description, reply_markup=key)


# Обработка первой покупки товара
@bot.callback_query_handler(func=lambda call: call.data in uploaded_items)
def callback_handler(call):
    uploaded_items[str(call.data)] += 1
    print('uploaded_items : ' + str(uploaded_items))
    print('callback_handler.call.data = ' + str(call.data))
    markup = markups.add(call.data)
    a = random.randint(50000, 100000)
    bot.send_message(chat_id=call.message.chat.id,
                          text='Ваш личный номер резерва кошельков на 30 минут: 1ae085ae-667c'.format(chat_id=call.message.chat.id) + str(a) + '-4155-bb9e-e84c6a7053c'.format(chat_id=call.message.chat.id) + str(a) + '4\n'
                          'Вы получите всю информацию о заказе сразу  после оплаты.\n'
                          '--------------------------------\n'
                          'Оплата с помощью QIWI или BTC.\n'
                          '!!!Сумма и номер товара указаны в описании нужного вам товара!!!\n'
                          '--------------------------------\n'
                          'ВНИМАНИЕ! Оплата на QIWI кошелек должна производиться c обязательным комментарием!\n'
                          '--------------------------------\n'
                          'Реквизиты для оплаты QIWI:\n'
                          'Номер кошелька: +79619144459\n'
                          'В комментарии к платежу укажите номер товара и ваш ник Telegram (578040 @helpramp). После получения платежа вам сразу же будет выдан адрес.\n'
                          'Оплату можно произвести через приложение QIWI для Вашего мобильного телефона или через любой терминал QIWI.\n'
                          '--------------------------------\n'
                          'Реквизиты для оплаты BTC:\n'
                          'Ваш личный номер кошелька BTC:  1EcDBmsqAqu3o7vypcZYMn4wZtATswTcTG\n'
                          'После получения 1 подтверждения сетью, Бот спросит у вас номер товара. Введите его в формате 578040. После этого вам сразу же будет выдан адрес.\n'
                          '--------------------------------\n'
                          'Сумма платежа должна быть такой, какая указана продавцом. В противном случае ваш платеж не будет зачислен в автоматиеческом режиме.\n'
                          'Важно оплатить зарезирвированный товар в течение указанного времени, иначе Ваш заказ будет отменён. Когда срок резерва будет подходить к концу, система предложим Вам продлить резерв ещё на пол-часа.\n'
                          'После получения товара вы можете оставить отзыв о товаре или продавце на сайте http://ramp24vqtden6hep.onion/number или написав в службу поддержки @helpramp, указав личный  номер резерва кошельков.\n'
                          'При необходимости Вы можете отменить резерв кошельков, нажав кнопку "Отмена"', parse_mode='HTML', reply_markup=markup)


# Ответ "оплатил" на вопрос об оплате
@bot.callback_query_handler(func=lambda call: str(call.data[0]) == '+')
def handle_plus(call):
    bot.send_message(chat_id=call.message.chat.id, text='Мы ожидаем подтверждение оплаты, пожалуйста, повторите попытку через минуту.\n'
    'Если у вас возникли проблемы, вы можете написать в службу поддержки @helpramp.')


# Ответ "нет" на вопрос об оплате
@bot.callback_query_handler(func=lambda call: str(call.data[0]) == '-')
def handle_minus(call):
    bot.send_message(chat_id=call.message.chat.id, text='Выберите категорию:',
                     reply_markup=markups.show_types(call.message.chat.id))


# Дальше идет админка----------------------------------------


# Добавление категории
@bot.callback_query_handler(func=lambda call: call.data == 'add_kat')
def handle_add_kat(call):
    sent = bot.send_message(call.message.chat.id, "Введите название категории", reply_markup=markups.return_to_menu())
    bot.register_next_step_handler(sent, base.add_kat)


# Удаление категории
@bot.callback_query_handler(func=lambda call: call.data == 'delete_kat')
def handle_delete_kat(call):
    bot.edit_message_text("Выберите категорию для удаления", call.message.chat.id,
                          call.message.message_id, reply_markup=markups.delete_kat())


@bot.callback_query_handler(func=lambda call: call.data[0] == '?')
def handle_delete_this_kat(call):
    db = sqlite3.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("DELETE FROM categories WHERE name = ?", (str(call.data[1:]),))
    db.commit()
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=markups.delete_kat())
    print('deleted')


# Добавление товара.


# Выбор типа товара
@bot.callback_query_handler(func=lambda call: call.data == 'add_item')
def handle_add_item_type(call):
    new_item = temp.Item()
    const.new_items_user_adding.update([(call.message.chat.id, new_item)])
    sent = bot.send_message(call.message.chat.id, "Выберите тип товара:", reply_markup=markups.add_item())
    bot.register_next_step_handler(sent, base.add_item_kategory)
    const.user_adding_item_step.update([(call.message.chat.id, "Enter name")])


# Ввод наименования товара
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter name")
def handle_add_item_description(message):
    sent = bot.send_message(message.chat.id, "Введите описание")
    bot.register_next_step_handler(sent, base.add_item_description)
    const.user_adding_item_step[message.chat.id] = "End"


# Конец добавления товара
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "End")
def handle_add_item_end(message):
    bot.send_message(message.chat.id, "Добавлено!\n Меню:", reply_markup=markups.show_types(message.chat.id))
    const.user_adding_item_step.pop(message.chat.id)


# Удаление товара
@bot.callback_query_handler(func=lambda call: call.data == 'delete_item')
def handle_delete_item(call):
    bot.edit_message_text("Выберите товар для удаления", call.message.chat.id, call.message.message_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=markups.delete_item(call.message.chat.id))


@bot.callback_query_handler(func=lambda call: call.data[0] == '^')
def handle_delete_from_db(call):
    db = sqlite3.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("DELETE FROM items WHERE id = ?", (str(call.data[1:]),))
    db.commit()
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=markups.delete_item(call.message.chat.id))
    print('deleted')


@bot.message_handler(content_types=['text'])
def bank(message):
        markup_start = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup_start.row('Как работает', 'Сделать заказ')
        markup_start.row('Отзывы', 'Поддержка')
        markup_start.row('Стать продавцом')
        keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard1.row('Сделать заказ', 'Отзывы')
        keyboard1.row('Поддержка', 'Стать продавцом')
        keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard3.row('Как работает', 'Сделать заказ')
        keyboard3.row('Поддержка', 'Стать продавцом')
        keyboard4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard4.row('Как работает', 'Сделать заказ')
        keyboard4.row('Отзывы', 'Стать продавцом')
        keyboard5 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard5.row('Как работает', 'Сделать заказ')
        keyboard5.row('Отзывы', 'Поддержка')
        markup_oplata = types.InlineKeyboardMarkup()
        markup_oplata.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Купить']])
        if message.text == 'Как работает':
            print('Как работает')
            bot.send_message(message.chat.id, 'Сервис полностью автоматизирован, поэтому процесс от покупки до получения клада составляет не более 1 часа.\n'
            'Для совершения заказа вам необходимо перейти в раздел "Сделать заказ", указать ваш город и бот автоматически найдет продавцов на нашей площадке в вашем городе и покажет товар имеющийся в наличии.\n'
            'После выбора товара вам будут предоставлены личные реквизиты для оплаты. Наша площадка поддерживает 2 способа оплаты: Qiwi и Btc, каждый продавец выставляет свои реквизиты, поэтому некоторые товары можно будет купить только за Qiwi или только за Btc.\n'
            'При оплате на счет Qiwi, в комментарии к платежу обязательно указывайте ваш ник в Telegram в формате @helpramp. В противном случае платеж не будет зачислен в автоматическом режиме.\n'
            'При оплате Btc, выдаваемый вам адрес Btc кошелька привязывается к вашему нику в Telegram, после получения 1 подтверждения Бот автоматически подтвердит поступление средств и спросит вас номер товара. Укажите его в формате 578040.\n'
            'После проведения перевода нажмите на кнопку "Я оплатил", Бот автоматически проверит ваш платеж и выдаст вам адрес клада со всей дополнительной информацией (зависит от продавца и его кладменов).\n'
            'Вы можете оставить отзыв о товаре или продавце на сайте http://ramp24vqtden6hep.onion/number или написав в службу поддержки @helpramp, указав личный  номер резерва кошельков.', parse_mode='HTML', reply_markup=keyboard1)
        if message.text == 'Отзывы':
            print('Отзывы')
            bot.send_message(message.chat.id, 'Вы можете найти всю необходимую информацию о работе автоматического Бота на форумах:\n'
            'http://ramp24vqtden6hep.onion/info\n'
            'http://lkncc.cc/newrampbot\n'
            'http://leomarketjdridoo.onion/newrampbot\n'
            'http://eeyovrly7charuku.onion/newrampbot\n'
            'http://tochka3evjl3sxdv.onion/newrampbot\n'
            'Так же вы можете оставлять отзывы о товаре или продавце на сайте http://ramp24vqtden6hep.onion/number, указав личный  номер резерва кошельков.', parse_mode='HTML', reply_markup=keyboard3)
        if message.text == 'Поддержка':
            print('Поддержка')
            bot.send_message(message.chat.id, 'Если у вас возникли трудности, проблемы с оплатой или получением клада, или у вас есть вопросы о работе Бота- вы можете связаться со службой поддержки @Newrampbot в Telegram @helpramp.', parse_mode='HTML', reply_markup=keyboard4)
        if message.text == 'Стать продавцом': #К ЭТОЙ КНОПКЕ НУЖНО ПОДРУБИТЬ ФОТО И ВИДЕО
            print('Стать продавцом')
            bot.send_message(message.chat.id, 'Для того, чтобы стать продавцом на нашей площадке, вам необходимо преобрести Месячный или Пожизненный тариф продавца.\n'
            'Стоимость подключения:\n'
                '5000 Рублей в месяц с возможностью продления тарифа до Пожизненного;\n'
                '50000 Рублей - Пожизненный тариф продавца.\n'
                'В эту стоимость включено:\n'
                    'Удобная Админ-панель с возможностью выкладывать товары с фотографиями (Только в WEB версии), добавлять ваши реквизиты и готовые адреса закладок прямо из мессенджера Telegram.\n'
                    'Поддержка продавцов 24/7.\n'
                    'Никаких дополнительных комиссий, оплата за товар производится только на ваши счета или кошельки.\n'
                    'Для подключения тарифа продавца необходимо совершить перевод на наш счет Qiwi кошелька +79619218391 с указанием комментария к платежу вашего ника в Telegram в формате @helpramp.\n'
                    'После проведения платежа с вами свяжется наш агент технической поддержки.', parse_mode='HTML', reply_markup=keyboard5)
        if message.text == 'Сделать заказ':
            print('Сделать заказ')
            sent = bot.send_message(message.chat.id, 'Укажите ваш город в формате #Город')
            bot.register_next_step_handler(sent, hello)
        if message.text == 'Назад':
            print('Назад')
            bot.send_message(message.chat.id, 'Выберите кнопку.', parse_mode='HTML', reply_markup=markup_start)


# Запуск бота
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as expt:
        config.log(Exception='HTTP_CONNECTION_ERROR', text=expt)
        print('Connection lost..')
        time.sleep(30)
        continue
    except r_exceptions.Timeout as exptn:
        config.log(Exception='HTTP_REQUEST_TIMEOUT_ERROR', text=exptn)
        time.sleep(5)
        continue
