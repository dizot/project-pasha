import sqlite3 as sl
from data_base import cafe_db
import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import config


dt2 = time.time()

con = sl.connect('cafe.db',check_same_thread = False)


bot = telebot.TeleBot(config.token)


dict_category = {}
def category():
    with con:
        cat = con.execute("SELECT * FROM Category")
        for i in cat.fetchall():
            dict_category[i[0]] = i[1]
category()

dict_dish = {}
def dish():
    with con:
        d = con.execute("SELECT * FROM Menu")
        for i in d.fetchall():
            dict_dish[i[2]] = i[2], i[3], i[5], i[6], i[4]


dish()


def keyb_category():
    inline_markup_category = InlineKeyboardMarkup()
    for k, v in dict_category.items():
        inline_markup_category.add(InlineKeyboardButton((v), callback_data=f'c0{k}'))
    return inline_markup_category


def keyb_more():
    inline_markup_more = InlineKeyboardMarkup()
    inline_btn_11 = InlineKeyboardButton('Подробнее', callback_data=f'd0')
    inline_markup_more.add(inline_btn_11)
    return inline_markup_more


inline_markup_more2 = InlineKeyboardMarkup()
inline_btn_21 = InlineKeyboardButton('Добавить в корзину', callback_data='e0')
inline_btn_22 = InlineKeyboardButton('Меню', callback_data='e1')
inline_markup_more2.add(inline_btn_21, inline_btn_22)

inline_markup_basket = InlineKeyboardMarkup()
inline_btn_23 = InlineKeyboardButton('Корзина', callback_data='e2')
inline_btn_26 = InlineKeyboardButton('Меню', callback_data='e5')
inline_markup_basket.add(inline_btn_23, inline_btn_26)


def change_basket():
    inline_markup_chan_basket = InlineKeyboardMarkup()
    inline_btn_24 = InlineKeyboardButton('Удалить', callback_data='e3')
    inline_btn_25 = InlineKeyboardButton('Изменить', callback_data='e4')
    inline_markup_chan_basket.add(inline_btn_24, inline_btn_25)
    return inline_markup_chan_basket


def accept_basket():
    inline_markup_accept_basket = InlineKeyboardMarkup()
    inline_btn_27 = InlineKeyboardButton('Оформить заказ', callback_data='e6')
    inline_btn_28 = InlineKeyboardButton('Удалить заказ', callback_data='e7')
    inline_markup_accept_basket.add(inline_btn_27, inline_btn_28)
    return inline_markup_accept_basket


def receiving():
    inline_markup_receiving = InlineKeyboardMarkup()
    inline_btn_29 = InlineKeyboardButton('Доставка', callback_data='e8')
    inline_btn_30 = InlineKeyboardButton('Ресторан', callback_data='e9')
    inline_markup_receiving.add(inline_btn_29, inline_btn_30)
    return inline_markup_receiving


def accept_ad():
    inline_markup_accept_ad = InlineKeyboardMarkup()
    inline_btn_36 = InlineKeyboardButton('Подтвердить адрес', callback_data='f5')
    inline_btn_37 = InlineKeyboardButton('Изменить адрес', callback_data='f6')
    inline_markup_accept_ad.add(inline_btn_36, inline_btn_37)
    return inline_markup_accept_ad


dict_basket = {}
dict_basket2 = {}
dict_basket3 = {}

def amount(message):
    try:
        a = int(message.text)
        if a > 0:
            dict_basket[message.from_user.id]['amount'] = a
            bot.send_message(message.chat.id, "Товар добавлен в корзину", reply_markup=inline_markup_basket)
        else:
            bot.send_message(message.chat.id, "Введено неверное количество, добавьте товар заново")
    except:
        bot.send_message(message.chat.id, "Введено неверное количество, добавьте товар заново")

    for k, v in dict_basket.items():
        dict_basket2[v['name']] = {v['price']: v['amount']}
        dict_basket3[message.from_user.id] = {'sum': None}



def new_address(message):
    sql_change = f"""UPDATE Client_base SET address = '{message.text}' WHERE teleg_id = {message.from_user.id}"""
    with con:
        con.execute(sql_change)
    bot.send_message(message.chat.id, f"Ваш адрес успешно изменён\n\n Время доставки составит до 60 минут", reply_markup=keyb_payment())


def keyb_payment():
    inline_markup_keyb_payment = InlineKeyboardMarkup()
    inline_btn_38 = InlineKeyboardButton('Оплата наличными', callback_data='f7')
    inline_btn_39 = InlineKeyboardButton('Оплата картой', callback_data='f8')
    inline_markup_keyb_payment.add(inline_btn_38, inline_btn_39)
    return inline_markup_keyb_payment

dict_booking = {}
def keyb_rest():
    mass = ['1 стол / до 2 человек', '1 стол / до 4 человек', '1 стол / до 8 человек', '1 стол / до 12 человек',
            '2 стола / до 24 человек']

    inline_markup_table = InlineKeyboardMarkup()

    for i in mass:
        inline_markup_table.add(InlineKeyboardButton((i), callback_data=f'f9{i}'))
    return inline_markup_table



def keyb_rest2():
    mass = ['1 стол / до 2 человек', '1 стол / до 4 человек', '1 стол / до 8 человек', '1 стол / до 12 человек',
            '2 стола / до 24 человек']

    inline_markup_table = InlineKeyboardMarkup()

    for i in mass:
        inline_markup_table.add(InlineKeyboardButton((i), callback_data=f'g5{i}'))
    return inline_markup_table


def booking_time():
    dict_masstime = {'10.00': '11.00', '12.00': '13.00', '14.00': '15.00', '16.00': '17.00', '18.00': '19.00', '20.00': '21.00' }

    inline_markup_booking_time = InlineKeyboardMarkup()

    for k, v in dict_masstime.items():
        inline_markup_booking_time.add(InlineKeyboardButton((k), callback_data=f'g1{k}'), InlineKeyboardButton((v), callback_data=f'g1{v}'))
    return inline_markup_booking_time


def change_booking():
    inline_markup_keyb_change_booking = InlineKeyboardMarkup(row_width=2)
    inline_btn_40 = InlineKeyboardButton('Изменить столик', callback_data='g2')
    inline_btn_41 = InlineKeyboardButton('Изменить время', callback_data='g3')
    inline_btn_42 = InlineKeyboardButton('Удалить бронь', callback_data='g4')
    inline_markup_keyb_change_booking.add(inline_btn_40, inline_btn_41, inline_btn_42)
    return inline_markup_keyb_change_booking









dict_users = {}

def users():
    dict_users[1111111] = {'name': 'паша карпов', 'telephone': '+375 44 343546', 'password': 'qwertyui12','address': 'улица Пушкина, дом 21, квартира 30'}
    dict_users[2323] = {'name': 'паша карпов'}
    # dict_users[810809759] = {'name': 'паша карпов', 'telephone': '+375 44 343546', 'password': 'qwertyui12', 'address': 'улица Пушкина, дом 21, квартира 30'}

    with con:
        client = con.execute("SELECT * FROM Client_base")
        for i in client.fetchall():
            dict_users[i[5]] = {'name': i[1], 'telephone': i[2], 'password': i[3], 'address': i[4]}

users()


inline_markup_registration = InlineKeyboardMarkup()
inline_btn_0 = InlineKeyboardButton('Зарегистрироваться', callback_data='a0')
inline_markup_registration.add(inline_btn_0)

inline_markup_del_mes = InlineKeyboardMarkup()
inline_btn_4 = InlineKeyboardButton('Удалить сообщение', callback_data='a4')
inline_markup_del_mes.add(inline_btn_4)

inline_markup_accept_del_mes = InlineKeyboardMarkup()
inline_btn_5 = InlineKeyboardButton('Удалить данные', callback_data='a5')
inline_btn_6 = InlineKeyboardButton('Отмена', callback_data='a6')
inline_markup_accept_del_mes.add(inline_btn_5, inline_btn_6)

inline_markup_change_data = InlineKeyboardMarkup(row_width=2)
inline_btn_10 = InlineKeyboardButton('ФИО', callback_data='b1')
inline_btn_20 = InlineKeyboardButton('Телефон', callback_data='b2')
inline_btn_30 = InlineKeyboardButton('Пароль', callback_data='b3')
inline_btn_40 = InlineKeyboardButton('Адрес', callback_data='b4')
inline_markup_change_data.add(inline_btn_10, inline_btn_20, inline_btn_30, inline_btn_40)




def registration_name(message):
    user_id = message.from_user.id
    dict_users[user_id] = {'name': message.text, 'telephone': None, 'password': None, 'address': None}


    telephone = bot.send_message(message.chat.id, "Введите телефон")
    bot.register_next_step_handler(telephone, registration_tel)

def registration_tel(message):
    user_id = message.from_user.id
    dict_users[user_id] = {'name': dict_users[user_id]['name'], 'telephone': message.text, 'password': None, 'address': None}


    password = bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(password, registration_pas)


def registration_pas(message):
    user_id = message.from_user.id
    dict_users[user_id] = {'name': dict_users[user_id]['name'], 'telephone': dict_users[user_id]['telephone'], 'password': message.text, 'address': None}


    address = bot.send_message(message.chat.id, "Введите адрес доставки")
    bot.register_next_step_handler(address, registration_address)


inline_markup_user_data = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton('Показать мои данные', callback_data='a1')
inline_btn_2 = InlineKeyboardButton('Изменить мои данные', callback_data='a2')
inline_btn_3 = InlineKeyboardButton('Удалить мои данные', callback_data='a3')
inline_markup_user_data.add(inline_btn_1)
inline_markup_user_data.add(inline_btn_2, inline_btn_3)

def registration_address(message):
    user_id = message.from_user.id
    dict_users[user_id] = {'name': dict_users[user_id]['name'], 'telephone': dict_users[user_id]['telephone'], 'password': dict_users[user_id]['password'], 'address': message.text}
    print(dict_users)
    bot.send_message(message.chat.id, "Регистрация прошла успешна", reply_markup=inline_markup_user_data)

    sql_insert = "INSERT INTO Client_base (name, telephone, password, address, teleg_id) values(?, ?, ?, ?, ?)"

    k = dict_users[user_id]
    string = [(f"{k['name']}", f"{k['telephone']}", f"{k['password']}", f"{k['address']}", f"{user_id}")]


    with con:
        con.executemany(sql_insert, string)


def new_name2(message):
    dict_users[message.from_user.id]['name'] = message.text
    bot.send_message(message.chat.id, "ФИО успешно изменены")

    sql_change = f"""UPDATE Client_base 
    SET name = '{dict_users[message.from_user.id]['name']}' WHERE teleg_id = {message.from_user.id}"""
    with con:
        con.execute(sql_change)


def new_tel(message):
    dict_users[message.from_user.id]['telephone'] = message.text
    bot.send_message(message.chat.id, "Телефон успешно изменён")

    sql_change = f"""UPDATE Client_base 
        SET telephone = '{dict_users[message.from_user.id]['telephone']}' WHERE teleg_id = {message.from_user.id}"""
    with con:
        con.execute(sql_change)


def new_pas(message):
    dict_users[message.from_user.id]['password'] = message.text
    bot.send_message(message.chat.id, "Пароль успешно изменён")

    sql_change = f"""UPDATE Client_base 
        SET password = '{dict_users[message.from_user.id]['password']}' WHERE teleg_id = {message.from_user.id}"""
    with con:
        con.execute(sql_change)


def new_add(message):
    dict_users[message.from_user.id]['address'] = message.text
    bot.send_message(message.chat.id, "Адрес успешно изменён")

    sql_change = f"""UPDATE Client_base 
        SET address = '{dict_users[message.from_user.id]['address']}' WHERE teleg_id = {message.from_user.id}"""
    with con:
        con.execute(sql_change)




dict_admins = {}
dict_forward = {}
dict_data = {}
dict_del ={}


# словарь админов
def check_admin2():

    dict_admins[810809759] = {'user_name': 'pasha', 'rights': True}
    dict_admins[647012868] = {'user_name': 'UITAAP22', 'rights': False}


check_admin2()

# главная клавиатура
inline_markup_main = InlineKeyboardMarkup()
inline_btn_33 = InlineKeyboardButton('Список администраторов', callback_data='x1')
inline_btn_11 = InlineKeyboardButton('Изменить администратора', callback_data='x2')
inline_btn_22 = InlineKeyboardButton('Удалить администратора', callback_data='x3')
inline_markup_main.add(inline_btn_33)
inline_markup_main.add(inline_btn_11)
inline_markup_main.add(inline_btn_22)



inline_markup_n_admin = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton('Администратор', callback_data='x4')
inline_btn_2 = InlineKeyboardButton('Супер администратор', callback_data='x5')
inline_markup_n_admin.add(inline_btn_1, inline_btn_2)



inline_markup_del_admin = InlineKeyboardMarkup()
inline_btn_del_admin = InlineKeyboardButton('Удалить', callback_data='x6')
inline_btn_del_admin2 = InlineKeyboardButton('Отмена', callback_data='x7')
inline_markup_del_admin.add(inline_btn_del_admin, inline_btn_del_admin2)



inline_markup_change_ad = InlineKeyboardMarkup()
inline_btn_change_ad1 = InlineKeyboardButton('Изменить', callback_data='o0')
inline_btn_change_ad2 = InlineKeyboardButton('Отмена', callback_data='p0')
inline_markup_change_ad.add(inline_btn_change_ad1, inline_btn_change_ad2)



# изменение админов
def keyb_change_ad():
    inline_markup_change_ad2 = InlineKeyboardMarkup()
    for k, v in dict_admins.items():
        inline_markup_change_ad2.add(InlineKeyboardButton((v['user_name']), callback_data=f'o1{k}'))
    return inline_markup_change_ad2

# удаление админов
def keyb_del_ad():
    inline_markup_del_ad2 = InlineKeyboardMarkup()
    for k, v in dict_admins.items():
        inline_markup_del_ad2.add(InlineKeyboardButton((v['user_name']), callback_data=f'n0{k}'))
    return inline_markup_del_ad2


inline_markup_delete_admin = InlineKeyboardMarkup()
inline_btn_del_adminn = InlineKeyboardButton('Удалить', callback_data='n1')
inline_markup_delete_admin.add(inline_btn_del_adminn)



inline_markup_change_admin = InlineKeyboardMarkup()
inline_btn_change_admin1 = InlineKeyboardButton('Изменить имя', callback_data='t0')
inline_btn_change_admin2 = InlineKeyboardButton('Изменить права', callback_data='y0')
inline_markup_change_admin.add(inline_btn_change_admin1, inline_btn_change_admin2)



inline_markup_rights_admin = InlineKeyboardMarkup()
inline_btn_right_admin1 = InlineKeyboardButton('Администратор', callback_data='t1')
inline_btn_right_admin2 = InlineKeyboardButton('Супер администратор', callback_data='y1')
inline_markup_rights_admin.add(inline_btn_right_admin1, inline_btn_right_admin2)



@bot.message_handler(content_types=['text'])
def start(message):


    if message.text == '/start':
        user_id = message.from_user.id
        if user_id in dict_users:
            bot.send_message(message.chat.id, "Вот меню, выберите категорию", reply_markup=keyb_category())
        else:
            bot.send_message(message.chat.id, "Вы не зарегистрированы, пройдите регистрацию", reply_markup=inline_markup_registration)

    if message.text == '/my_data':
        if message.from_user.id in dict_users:
            bot.send_message(message.chat.id, "Ваши данные", reply_markup=inline_markup_user_data)
        else:
            bot.send_message(message.chat.id, "Сначала зарегистрируйтесь: /start")

    if message.text == '/menu':
        user_id = message.from_user.id
        if user_id in dict_users:
            bot.send_message(message.chat.id, "Вот меню, выберите категорию", reply_markup=keyb_category())
        else:
            bot.send_message(message.chat.id, "Вы не зарегистрированы, пройдите регистрацию",
                             reply_markup=inline_markup_registration)

    if message.text == '/admin':
        check_admin(message)

    if message.text == '/newadmin':
        if message.chat.id in dict_admins and dict_admins[message.chat.id]['rights'] == True:
            bot.send_message(message.chat.id, "Перешлите сообщение и укажите уровень прав нового администратора")
    new_admin(message)


    if message.text == '/help':
        bot.send_message(message.chat.id, f"/my_data - ваши данные\n/menu - меню")


    if message.text == '/help' and message.chat.id in dict_admins and dict_admins[message.chat.id]['rights'] == True:
        bot.send_message(message.chat.id, f"/admin - панель администратора\n/newadmin - добавление администратора")

# добваление администаторов
def new_admin(message):
    if message.chat.id in dict_admins and dict_admins[message.chat.id]['rights'] == True:
        try:
            forward_id = message.forward_from.id

            forward_username = message.forward_from.username

            dict_forward[message.chat.id] = forward_id, forward_username

            bot.send_message(message.chat.id, "Укажите уровень прав", reply_markup=inline_markup_n_admin)

        except:
            pass

# проверка на админа
def check_admin(message):
    try:
        if message.chat.id in dict_admins and dict_admins[message.chat.id]['rights'] == True:
            bot.send_message(message.chat.id, "Вы супер администратор", reply_markup=inline_markup_main)
    except:
        pass

    try:
        if message.chat.id in dict_admins and dict_admins[message.chat.id]['rights'] == False:
            bot.send_message(message.chat.id, "Вы администратор")
    except:
        pass

    try:
        if message.chat.id not in dict_admins:
            bot.send_message(message.chat.id, "Вы не админостратор")
    except:
        pass

# изменение имени админа
def new_name_ad(message):
    dict_admins[int(dict_data[message.chat.id])] = {'user_name': message.text,'rights': dict_admins[int(dict_data[message.chat.id])]['rights']}
    bot.send_message(message.chat.id, "Администратор изменён")


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, )
    id = call.message.chat.id
    flag = call.data[0:2]
    data = call.data[2:]


    if flag == 'c0':
        with con:
            dish = con.execute("SELECT * FROM Menu WHERE amount > 0")
            for i in dish.fetchall():
                if i[1] == int(data):
                    photo = open(f"data_base\{i[4]}", 'rb')
                    bot.send_photo(id, photo, f"{i[2]}", reply_markup=keyb_more())


    if flag == 'd0':
        name = call.message.caption
        if name != None:
            n = dict_dish[name]
            bot.edit_message_caption(f"Название: {n[0]}\nЦена: {n[1]} BYN\nОписание: {n[2]}\nВремя приготавления: {n[3]}\n", chat_id=id, message_id=call.message.message_id, reply_markup=inline_markup_more2)


    if flag == 'e0':
        a = call.message.caption
        b = a.split("\n")
        dict_basket[call.message.chat.id] = {'name': b[0], 'price': b[1], 'amount': None}

        am = bot.send_message(id, "Введите количество")
        bot.register_next_step_handler(am, amount)


    if flag =='e1':
        bot.send_message(id, "Выберите категорию", reply_markup=keyb_category())


    if flag == 'e2':
        all_sum = 0
        for k, v in dict_basket2.items():
            for k1, v1 in v.items():
                if v1 == None:
                    pass
                else:
                    a = k1.split(' ')
                    sum = float(a[1])*int(v1)
                    all_sum += (round(sum, 1))
                    bot.send_message(id, f"Ваша корзина: \n{k}\n{k1}\nКоличество: {v1}\nСумма: {round(sum, 1)} BYN", reply_markup=change_basket())
        if all_sum == 0:
            bot.send_message(id, f"Ваша корзина пуста, выберите что-нибудь из меню\n /menu")
        else:
            bot.send_message(id, f"Общая сумма заказа: {round(all_sum, 1)} BYN\nХотите подтвердить заказ?", reply_markup=accept_basket())
        if all_sum > 0:
            dict_basket3[call.message.chat.id]['sum'] = round(all_sum, 1)


    if flag == 'e3':
        try:
            a = call.message.text
            b = a.split("\n")
            dict_basket2.pop(b[1])
            bot.delete_message(id, call.message.message_id)
        except:
            pass


    if flag == 'e4':
        a = call.message.text
        b = a.split("\n")
        dict_basket[call.message.chat.id] = {'name': b[1], 'price': b[2], 'amount': None}

        new_a = bot.send_message(id, "Введите количество")
        bot.register_next_step_handler(new_a, amount)


    if flag == 'e5':
        bot.edit_message_text("Выберите категорию", chat_id=id, message_id=call.message.message_id, reply_markup=keyb_category())


    if flag == 'e6':
        bot.edit_message_text("Выберите способ получения заказа", chat_id=id, message_id=call.message.message_id, reply_markup=receiving())


    if flag == 'e7':
        bot.edit_message_text("Заказ удалён", chat_id=id, message_id=call.message.message_id)
        dict_basket2.clear()

    if  flag == 'e8':
        with con:
            address = con.execute(f"SELECT address FROM Client_base WHERE teleg_id = {call.message.chat.id}")
            for i in address.fetchall():
                for i1 in i:
                    bot.edit_message_text(f"Ваш адрес: {i1}?", chat_id=id, message_id=call.message.message_id, reply_markup=accept_ad())

    if flag == 'e9':
        bot.edit_message_text("Выберите нужный вариант", chat_id=id, message_id=call.message.message_id, reply_markup=keyb_rest())


    if flag == 'f5':
        bot.edit_message_text(f"Время доставки составит до 60 минут\n\nВыберите способ оплаты", chat_id=id, message_id=call.message.message_id, reply_markup=keyb_payment())

    if flag == 'f6':
        new_ad = bot.edit_message_text("Введите адрес", chat_id=id, message_id=call.message.message_id)
        bot.register_next_step_handler(new_ad, new_address)


    if flag == 'f7':
        bot.edit_message_text("Заказ успешно оформлен", chat_id=id, message_id=call.message.message_id)

        with con:
            mass_shop_num = []
            num = con.execute("SELECT shop_number FROM Order_list")
            for i in num.fetchall():
                for i1 in i:
                    mass_shop_num.append(i1)


        mass = []
        mass_id = []
        for k, v in dict_basket2.items():
            a = k.split(': ')
            mass.append(a[1])

            for k1, v1 in v.items():
                b = k1.split(': ')
                mass.append(b[1])
                mass.append(v1)


                mass2 = []
                with con:
                    d = con.execute(f"""SELECT id FROM Client_base WHERE teleg_id = {id}""")

                    for i in d.fetchall():
                        for i1 in i:
                            mass2.append(i1)
                            mass_id.append(i1)

                with con:
                    d = con.execute(f"""SELECT id FROM Menu WHERE name = '{mass[0]}'""")

                    for i in d.fetchall():
                        for i1 in i:
                            mass2.append(i1)
                mass2.append(mass[2])

                mass.clear()

                sql_insert = "INSERT INTO Order_list (client_id, dish, amount, shop_number) values(?, ?, ?, ?)"
                with con:
                    con.execute(sql_insert, [mass2[0], mass2[1], mass2[2], (mass_shop_num[-1] + 1)])


        for x in dict_basket3.values():
            for d in x.values():
                mass.append(d)


        sql_insert2 = "INSERT INTO Orders (client_id, date, delivery_time, order_price, way_to_get, shop_number) values(?, ?, ?, ?, ?, ?)"
        with con:
            con.execute(sql_insert2, [mass_id[0], dt2, '60 минут', mass[0], 'доставка', (mass_shop_num[-1] + 1)])

        dict_basket2.clear()


    if flag == 'f8':
        bot.edit_message_text("Заказ успешно оформлен", chat_id=id, message_id=call.message.message_id)

        with con:
            mass_shop_num = []
            num = con.execute("SELECT shop_number FROM Order_list")
            for i in num.fetchall():
                for i1 in i:
                    mass_shop_num.append(i1)


        mass = []
        mass_id = []
        for k, v in dict_basket2.items():
            a = k.split(': ')
            mass.append(a[1])

            for k1, v1 in v.items():
                b = k1.split(': ')
                mass.append(b[1])
                mass.append(v1)


                mass2 = []
                with con:
                    d = con.execute(f"""SELECT id FROM Client_base WHERE teleg_id = {id}""")

                    for i in d.fetchall():
                        for i1 in i:
                            mass2.append(i1)
                            mass_id.append(i1)

                with con:
                    d = con.execute(f"""SELECT id FROM Menu WHERE name = '{mass[0]}'""")

                    for i in d.fetchall():
                        for i1 in i:
                            mass2.append(i1)
                mass2.append(mass[2])

                mass.clear()

                sql_insert = "INSERT INTO Order_list (client_id, dish, amount, shop_number) values(?, ?, ?, ?)"
                with con:
                    con.execute(sql_insert, [mass2[0], mass2[1], mass2[2], (mass_shop_num[-1] + 1)])


        for x in dict_basket3.values():
            for d in x.values():
                mass.append(d)


        sql_insert2 = "INSERT INTO Orders (client_id, date, delivery_time, order_price, way_to_get, shop_number) values(?, ?, ?, ?, ?, ?)"
        with con:
            con.execute(sql_insert2, [mass_id[0], dt2, '60 минут', mass[0], 'доставка', (mass_shop_num[-1] + 1)])

        dict_basket2.clear()



    if flag == 'f9':
        id = call.message.chat.id
        dict_booking[id] = {'table': data, 'time': None}
        bot.edit_message_text("Выберите подходящее время", chat_id=id, message_id=call.message.message_id, reply_markup=booking_time())





    if flag == 'g1':
        id = call.message.chat.id
        dict_booking[id]['time'] = data
        bot.edit_message_text(f"Ваш столик зарезервирован:\n{dict_booking[id]['table']}\nВремя: {dict_booking[id]['time']}",
                              chat_id=id, message_id=call.message.message_id, reply_markup=change_booking())


        with con:
            mass_shop_num = []
            num = con.execute("SELECT shop_number FROM Order_list")
            for i in num.fetchall():
                for i1 in i:
                    mass_shop_num.append(i1)


        mass = []
        mass_id = []
        for k, v in dict_basket2.items():
            a = k.split(': ')
            mass.append(a[1])

            for k1, v1 in v.items():
                b = k1.split(': ')
                mass.append(b[1])
                mass.append(v1)


                mass2 = []
                with con:
                    d = con.execute(f"""SELECT id FROM Client_base WHERE teleg_id = {id}""")

                    for i in d.fetchall():
                        for i1 in i:
                            mass2.append(i1)
                            mass_id.append(i1)

                with con:
                    d = con.execute(f"""SELECT id FROM Menu WHERE name = '{mass[0]}'""")

                    for i in d.fetchall():
                        for i1 in i:
                            mass2.append(i1)
                mass2.append(mass[2])

                mass.clear()

                sql_insert = "INSERT INTO Order_list (client_id, dish, amount, shop_number) values(?, ?, ?, ?)"
                with con:
                    con.execute(sql_insert, [mass2[0], mass2[1], mass2[2], (mass_shop_num[-1] + 1)])

        for x in dict_basket3.values():
            for d in x.values():
                mass.append(d)

        sql_insert2 = "INSERT INTO Orders (client_id, date, delivery_time, order_price, way_to_get, shop_number, order_table) values(?, ?, ?, ?, ?, ?, ?)"
        with con:
            con.execute(sql_insert2, [mass_id[0], dt2, dict_booking[id]['time'], mass[0], 'ресторан', (mass_shop_num[-1] + 1), dict_booking[id]['table']])




    if flag == 'g2':
        bot.edit_message_text("Выберите нужный вариант", chat_id=id, message_id=call.message.message_id, reply_markup=keyb_rest2())


    if flag == 'g3':
        with con:
            con.execute(f"""DELETE FROM Orders WHERE delivery_time = {dict_booking[id]['time']}""")

        id = call.message.chat.id
        dict_booking[id]['time'] = data
        bot.edit_message_text("Выберите подходящее время", chat_id=id, message_id=call.message.message_id, reply_markup=booking_time())


    if flag == 'g4':
        with con:
            con.execute(f"""DELETE FROM Orders WHERE delivery_time = {dict_booking[id]['time']}""")
        bot.edit_message_text("Бронь удалена", chat_id=id, message_id=call.message.message_id)
        dict_booking.clear()


    if flag == 'g5':
        with con:
            con.execute(f"""DELETE FROM Orders WHERE delivery_time = {dict_booking[id]['time']}""")
        id = call.message.chat.id
        dict_booking[id] = {'table': data, 'time': dict_booking[id]['time']}
        bot.edit_message_text(f"Ваш столик зарезервирован:\n{dict_booking[id]['table']}\nВремя: {dict_booking[id]['time']}",
                                chat_id=id, message_id=call.message.message_id, reply_markup=change_booking())


        with con:
            mass_shop_num = []
            num = con.execute("SELECT shop_number FROM Order_list")
            for i in num.fetchall():
                for i1 in i:
                    mass_shop_num.append(i1)

        mass = []
        mass_id = []
        for k, v in dict_basket2.items():
            a = k.split(': ')
            mass.append(a[1])

            for k1, v1 in v.items():
                b = k1.split(': ')
                mass.append(b[1])
                mass.append(v1)


                mass2 = []
                with con:
                    d = con.execute(f"""SELECT id FROM Client_base WHERE teleg_id = {id}""")

                    for i in d.fetchall():
                        for i1 in i:
                            mass2.append(i1)
                            mass_id.append(i1)

                with con:
                    d = con.execute(f"""SELECT id FROM Menu WHERE name = '{mass[0]}'""")

                    for i in d.fetchall():
                        for i1 in i:
                            mass2.append(i1)
                mass2.append(mass[2])

                mass.clear()

                sql_insert = "INSERT INTO Order_list (client_id, dish, amount, shop_number) values(?, ?, ?, ?)"
                with con:
                    con.execute(sql_insert, [mass2[0], mass2[1], mass2[2], (mass_shop_num[-1] + 1)])

        for x in dict_basket3.values():
            for d in x.values():
                mass.append(d)

        sql_insert2 = "INSERT INTO Orders (client_id, date, delivery_time, order_price, way_to_get, shop_number, order_table) values(?, ?, ?, ?, ?, ?, ?)"
        with con:
            con.execute(sql_insert2, [mass_id[0], dt2, dict_booking[id]['time'], mass[0], 'ресторан', (mass_shop_num[-1] + 1), dict_booking[id]['table']])

        dict_basket2.clear()

    if flag == 'a0':
        name = bot.edit_message_text("Введите ФИО", chat_id=id, message_id=call.message.message_id)
        bot.register_next_step_handler(name, registration_name)

    if flag == 'a1':
        user = dict_users[call.message.chat.id]
        bot.edit_message_text(
            f"Ваши данные:\nФИО: {user['name']}\nТелефон: {user['telephone']}\nПароль: {user['password']}\n"
            f"Адрес: {user['address']}\n", chat_id=id, message_id=call.message.message_id,
            reply_markup=inline_markup_del_mes)

    if flag == 'a4':
        bot.delete_message(id, call.message.message_id)

    if flag == 'a3':
        bot.edit_message_text("Вы действительно хотите удалить данные?", chat_id=id,
                              message_id=call.message.message_id, reply_markup=inline_markup_accept_del_mes)

    if flag == 'a5':
        dict_users.pop(call.message.chat.id)
        bot.delete_message(id, call.message.message_id)
        bot.send_message(id, "Ваши данные успешно удалены")

        with con:
            con.execute(f"""DELETE FROM Client_base WHERE teleg_id = {call.message.chat.id}""")

    if flag == 'a6':
        bot.delete_message(id, call.message.message_id)

    if flag == 'a2':
        bot.edit_message_text("Выберите, что хотите изменить", chat_id=id, message_id=call.message.message_id,
                              reply_markup=inline_markup_change_data)

    if flag == 'b1':
        name22 = bot.edit_message_text("Введите новые ФИО", chat_id=id, message_id=call.message.message_id)
        bot.register_next_step_handler(name22, new_name2)

    if flag == 'b2':
        tel = bot.edit_message_text("Введите новый телефон", chat_id=id, message_id=call.message.message_id)
        bot.register_next_step_handler(tel, new_tel)

    if flag == 'b3':
        pas = bot.edit_message_text("Введите новый пароль", chat_id=id, message_id=call.message.message_id)
        bot.register_next_step_handler(pas, new_pas)

    if flag == 'b4':
        add = bot.edit_message_text("Введите новый адрес", chat_id=id, message_id=call.message.message_id)
        bot.register_next_step_handler(add, new_add)










    if flag == 'x1':
        for k, v in dict_admins.items():
            bot.send_message(id, f"Имя пользователя: {v['user_name']} \nУровень прав: {v['rights']}")
        bot.edit_message_text("Вот все администраторы", chat_id=id, message_id=call.message.message_id)


    if flag == 'x2':
        bot.edit_message_text("Вы действительно хотите изменить администратора?", chat_id=id,
                              message_id=call.message.message_id, reply_markup=inline_markup_change_ad)


    if flag == 'o0':
        bot.edit_message_text("Выберите администратора, которого хотите изменить", chat_id=id,
                              message_id=call.message.message_id, reply_markup=keyb_change_ad())



    if flag == 'o1':
        dict_data[id] = data
        # print("dict_data", dict_data)
        bot.edit_message_text(f"Имя пользователя: {dict_admins[int(data)]['user_name']} \nУровень прав: "
                             f"{dict_admins[int(data)]['rights']}", chat_id=id,
                              message_id=call.message.message_id, reply_markup=inline_markup_change_admin)


    if flag == 't0':
        new_name = bot.edit_message_text("Укажите новое имя", chat_id=id, message_id=call.message.message_id)

        bot.register_next_step_handler(new_name, new_name_ad)
        with open('dict_admins.json', 'w', encoding='utf-8') as f:
            json.dump(dict_admins, f, ensure_ascii=False, indent=4)

        f = open('dict_admins.json', 'r', encoding='utf-8')
        d = json.loads(f.read())
        f.close()
        # print(d)
        # print(dict_admins)


    if flag == 'y0':
        bot.edit_message_text("Укажите права", chat_id=id, message_id=call.message.message_id,
                                         reply_markup=inline_markup_rights_admin)


        with open('dict_admins.json', 'w', encoding='utf-8') as f:
            json.dump(dict_admins, f, ensure_ascii=False, indent=4)

        f = open('dict_admins.json', 'r', encoding='utf-8')
        d = json.loads(f.read())
        f.close()
        # print(d)

    if flag == 't1':
        dict_admins[int(dict_data[id])] = {'user_name': dict_admins[int(dict_data[id])]['user_name'], 'rights': False}
        bot.edit_message_text("Администратор добавлен", chat_id=id, message_id=call.message.message_id)

        with open('dict_admins.json', 'w', encoding='utf-8') as f:
            json.dump(dict_admins, f, ensure_ascii=False, indent=4)

        f = open('dict_admins.json', 'r', encoding='utf-8')
        d = json.loads(f.read())
        f.close()
        # print(d)
        # print(dict_admins)


    if flag == 'y1':
        dict_admins[int(dict_data[id])] = {'user_name': dict_admins[int(dict_data[id])]['user_name'], 'rights': True}
        bot.edit_message_text("Супер администратор добавлен", chat_id=id, message_id=call.message.message_id)

        with open('dict_admins.json', 'w', encoding='utf-8') as f:
            json.dump(dict_admins, f, ensure_ascii=False, indent=4)

        f = open('dict_admins.json', 'r', encoding='utf-8')
        d = json.loads(f.read())
        f.close()
        # print(d)
        # print(dict_admins)


    if flag == 'p0':
        bot.send_message(id, "Отмена изменения")


    if flag == 'x3':
        bot.edit_message_text("Вы действительно хотите удалить администратора?", chat_id=id,
                              message_id=call.message.message_id, reply_markup=inline_markup_del_admin)


    if flag == 'x6':
        bot.edit_message_text("Выберите администратора, которого хотите удалить", chat_id=id,
                              message_id=call.message.message_id, reply_markup=keyb_del_ad())


    if flag == 'n0':
        dict_del[id] = data
        # print(dict_del)
        bot.edit_message_text(f"Имя пользователя: {dict_admins[int(data)]['user_name']} \nУровень прав: "
                             f"{dict_admins[int(data)]['rights']}", chat_id=id,
                              message_id=call.message.message_id, reply_markup=inline_markup_delete_admin)


    if flag == 'n1':
        dict_admins.pop(int(dict_del[id]))
        bot.edit_message_text("Администратор удалён", chat_id=id, message_id=call.message.message_id)
        with open('dict_admins.json', 'w', encoding='utf-8') as f:
            json.dump(dict_admins, f, ensure_ascii=False, indent=4)

        f = open('dict_admins.json', 'r', encoding='utf-8')
        d = json.loads(f.read())
        f.close()
        # print(d)
        # print(dict_admins)


    if flag == 'x7':
        bot.send_message(id, "Отмена удаления")


    if flag == 'x4':
        for k, v in dict_forward.values():
            pass
        dict_admins[k] = {'user_name': v, 'rights': False}
        bot.send_message(id, "Администратор добавлен")

        with open('dict_admins.json', 'w', encoding='utf-8') as f:
            json.dump(dict_admins, f, ensure_ascii=False, indent=4)

        f = open('dict_admins.json', 'r', encoding='utf-8')
        d = json.loads(f.read())
        f.close()
        # print(d)
        # print(dict_admins)
        dict_forward.popitem()


    if flag == 'x5':
        for k, v in dict_forward.values():
            pass
        dict_admins[k] = {'user_name': v, 'rights': True}
        bot.send_message(id, "Супер администратор добавлен")
        with open('dict_admins.json', 'w', encoding='utf-8') as f:
            json.dump(dict_admins, f, ensure_ascii=False, indent=4)

        f = open('dict_admins.json', 'r', encoding='utf-8')
        d = json.loads(f.read())
        f.close()
        # print(d)
        # print(dict_admins)
        dict_forward.popitem()



print("Ready")
bot.infinity_polling()