# -*- coding: utf-8 -*-?
import telebot
import temp, base


def start():
    markup = telebot.types.InlineKeyboardMarkup()
    btn_user = telebot.types.InlineKeyboardButton(text="��������!", callback_data='client_panel')
    btn_celler = telebot.types.InlineKeyboardButton(text="���������!", callback_data='celler_panel')
    markup.add(btn_celler, btn_user)
    return markup


def start1():
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('��� ��������', '������� �����')
    markup_start.row('������', '���������')
    markup_start.row('����� ���������')
    return markup_start


def show_types(user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    for key in base.give_menu():
        button = telebot.types.InlineKeyboardButton(text=key, callback_data=key)
        markup.add(button)
    if base.is_seller(user_id):
        btn_menu = telebot.types.InlineKeyboardButton(text="�����-������", callback_data='celler_panel')
        markup.add(btn_menu)
    return markup


def make_bill():
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row("����")
    markup.row("�������� �����")
    return markup


def return_to_menu():
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row("����")
    return markup


def is_seller():
    markup = telebot.types.InlineKeyboardMarkup()
    butquest = telebot.types.InlineKeyboardButton('����� ��� ����������?', callback_data='.')
    btn_y = telebot.types.InlineKeyboardButton('Yes', callback_data='&Yes')
    btn_n = telebot.types.InlineKeyboardButton('No', callback_data='&No')
    markup.row(butquest)
    markup.row(btn_n, btn_y)
    return markup


def add(id):
    markup = telebot.types.InlineKeyboardMarkup()
    butp = telebot.types.InlineKeyboardButton('� �������', callback_data='+' + str(id))
    butm = telebot.types.InlineKeyboardButton('������', callback_data='-' + str(id))
    markup.row(butp, butm)
    return markup


def edit():
    markup = telebot.types.InlineKeyboardMarkup()
    add_item = telebot.types.InlineKeyboardButton(text="�������� �����", callback_data='add_item')
    delete_item = telebot.types.InlineKeyboardButton(text="������� �����", callback_data='delete_item')
    add_kat = telebot.types.InlineKeyboardButton(text="�������� ���������", callback_data='add_kat')
    delete_kat = telebot.types.InlineKeyboardButton(text="������� ���������", callback_data='delete_kat')
    markup.row(add_kat, add_item)
    markup.row(delete_kat, delete_item)
    return markup


def add_item():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for category in base.give_menu():
        markup.add(category)
    return markup


def delete_item(user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    for item in base.find_users_items(user_id):
        btn_item = telebot.types.InlineKeyboardButton(text=item[5], callback_data="^" + str(item[0]))
        markup.add(btn_item)
    btn_menu = telebot.types.InlineKeyboardButton(text="��������� � �����-������", callback_data="celler_panel")
    markup.add(btn_menu)
    return markup


def delete_kat():
    markup = telebot.types.InlineKeyboardMarkup()
    for key in base.give_menu():
        button = telebot.types.InlineKeyboardButton(text=key, callback_data="?"+key)
        markup.add(button)
    btn_menu = telebot.types.InlineKeyboardButton(text="��������� � �����-������", callback_data="celler_panel")
    markup.add(btn_menu)
    return markup


def give_desc(id):
    print("in_murk")
    markup = telebot.types.InlineKeyboardMarkup()
    item = temp.item_finder(id)
    btn_buy = telebot.types.InlineKeyboardButton(text='������', callback_data=str(item.id))
    markup.row(btn_buy)