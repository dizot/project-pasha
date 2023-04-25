import sqlite3 as sl
import json
import time

con = sl.connect('cafe.db')


# Client_base
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS Client_base (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            telephone TEXT,
            password TEXT,
            address TEXT,
            teleg_id INTEGER,
            UNIQUE(telephone),
            UNIQUE(teleg_id),
            FOREIGN KEY (id) REFERENCES Orders (client_id)
        );
    """)

sql_insert = "INSERT INTO Client_base (name, telephone, password, address, teleg_id) values(?, ?, ?, ?, ?)"

test = [("Иванов Пётр", '+375 666 66 66', 'qwert123', 'улица Киселёва, дом 23, квартира 43', 813209759),
       ("Озерова Анастасия", '+375 456 66 6623', 'neasty', 'улица Карасёва, дом 57, квартира 90', 111809759),
       ("Киселёв Александр", '+375 324 66 662', 'adrei1234', 'улица Пушкина, дом 19, квартира 55', 777809759),
       ("Норманн Давид", '+375 666 78 66', 'david23d', 'улица Лермонтова, дом 17, квартира 58', 810889759),
       ("Jason Statham", '+375 56 66 55', 'mechanic', 'улица Киселёва, дом 31, квартира 15', 810800029),
       ("Jason Born", '+375 455 66 66', '123tqwer', 'улица Куйбышева, дом 23, квартира 72', 810856759),
       ('паша карпов', '+375 44 343546', 'qwertyui12', 'улица Пушкина, дом 21, квартира 30', 810809759)]
try:
    with con:
        con.executemany(sql_insert, test)






    # Category
    with con:
        con.execute("""
             CREATE TABLE IF NOT EXISTS Category (
                 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 FOREIGN KEY (id) REFERENCES Menu (category)
             );
         """)

    sql_insert = "INSERT INTO Category (name) values(?)"



    with con:
        con.execute(sql_insert, ["Закуски"])
        con.execute(sql_insert, ["Напитки"])
        con.execute(sql_insert, ["Горячие блюда"])
        con.execute(sql_insert, ["Пицца"])
        con.execute(sql_insert, ["Супы"])






    # Menu
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS Menu (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                category INTEGER,
                name TEXT,
                price INTEGER,
                picture TEXT,
                description TEXT,
                cooking_time INTEGER,
                amount INTEGER,
                FOREIGN KEY (id) REFERENCES Order_list (dish)
            );
        """)

    sql_insert = "INSERT INTO Menu (category, name, price, picture, description, cooking_time, amount) values(?, ?, ?, ?, ?, ?, ?)"

    test3 = [(1, "Луковые кольца", 7.9, "луковые кольца.jpg", "Луковые кольца, соус Барбекю с майонезом", "10 минут", 21),
            (2, "Лимонад Клюква-малина", 5.2, "Лимонад Клюква-малина.jpg", "Клюквенный морс, бонаква сильногазированная, клюква, тимьян, лимон", "5 минут", 12),
            (3, "Запеченные ньокки с цыпленком и грибами", 14.7, "Запеченные ньокки с цыпленком и грибами.jpg", "Картофельные ньокки, куриное филе, лук, шампиньоны, соус бешамель, сыр Моцарелла", "20 минут", 39),
            (4, "Баварская", 22, "Баварская.jpg", "Колбаски охотничьи, бекон, огурец маринованный, лук красный, соус Рэнч, соус горчичный, сыр Моцарелла, луковые чипсы, орегано", "15 минут",31),
            (5, "Борщ с копченым ребром", 9.6, "Борщ с копченым ребром.jpg", "Свиное копченое ребрышко, свекла, картофель, паста томатная, бульон, морковь, лук, чеснок, сметана, укроп", "15 минут", 0),
            (1, "Куриные наггетсы", 8.6, "Куриные наггетсы.jpg", "Куриные наггетсы с соусом кетчуп", "5 минут", 23),
            (1, "Запечённый Чеддер с соусом Роуз Мэри", 15.9, "Запечённый Чеддер.jpg", "Сыр Чеддер в панировке, соус Роуз Мэри, микс салатов, томат черри, масло базилик", "10 минут", 53),
            (1, "Карпаччо из говядины", 19.3, "Карпаччо из говядины.jpg", "Маринованная говядина, томат черри, салат руккола, сыр Пармезан, луковые чипсы, медовая заправка", "10 минут", 0),
            (2, "Латте Орео", 7, "Латте Орео.jpg", "Латте с молочным шоколадом и дробленым печеньем ОРЕО", "5 минут", 19),
            (2, "Айс Латте", 4.5, "Айс Латте.jpg", "Эспрессо, молоко, лед", "5 минут", 3),
            (3, "Чили окорочок с жареным картофелем 🌶", 15.7, "Чили окорочок с жареным картофелем.jpg", "Окорочок куриный, жареный картофель, капуста маринованная, соус Рэнч, соус Чили, петрушка", "20 минут", 23),
            (3, "Говядина c картофельными дольками и овощами на гриле", 29.7, "Говядина c картофельными дольками и овощами на гриле.jpg", "Филе говядины, картофельные дольки, овощи на гриле: цукини, шампиньоны, микс перцев, лук красный, томат черри, масло базилик", "20 минут", 30),
            (4, "Цыпленок карри", 17.9, "Цыпленок карри.jpg", "Цыпленок, ананасы, соус карри, красный лук, сладкий перец, моцарелла, томатный соус", "15 минут", 14),
            (4, "Четыре сезона", 17.9, "Четыре сезона.jpg", "Итальянские травы, томатный соус, томаты, пикантная пепперони, кубики брынзы, моцарелла, ветчина, шампиньоны", "15 минут", 19),
            (5, "Том Кха с цыпленком 🌶", 13.9, "Том Кха с цыпленком.jpg", "Бульон, кокосовое молоко, цыпленок-гриль, сливки, томаты черри, шампиньоны, лайм, перец чили, кинза, лук-порей, онигири. Острое", "15 минут", 16),
            (5, "Том Ям с лососем 🌶", 17.9, "Том Ям с лососем.jpg", "Куриный бульон, кокосовое молоко, филе лосося, сливки, грибы шиитаке, такуан, перец чили, кинза, лайм, онигири. Острое.", "15 минут", 9)]

    with con:
        con.executemany(sql_insert, test3)









    # Order_list
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS Order_list (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                dish INTEGER,
                amount INTEGER,
                shop_number,
                FOREIGN KEY (client_id) REFERENCES orders (client_id)
            );
        """)

    sql_insert = "INSERT INTO Order_list (client_id, dish, amount, shop_number) values(?, ?, ?, ?)"

    test4 = [(1, 1, 2, 1),
             (2, 2, 1, 2),
             (3, 3, 2, 3),
             (3, 5, 1, 4),
             (1, 4, 3, 5),
             (3, 5, 1, 6)]


    with con:
        con.executemany(sql_insert, test4)









    # Orders

    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                date INTEGER,
                delivery_time INTEGER,
                order_price INTEGER,
                way_to_get TEXT,
                shop_number INTEGER,
                order_table TEXT      
            );
        """)

    sql_insert = "INSERT INTO Orders (client_id, date, delivery_time, order_price, way_to_get, shop_number, order_table) values(?, ?, ?, ?, ?, ?, ?)"

    test5 = [(1, '2020-01-08T13:00:00.000Z', '2020-01-08T14:00:00.000Z', 70, "доставка", 1, 'NULL'),
             (2, '2020-09-08T10:00:00.000Z', '2020-09-08T11:00:00.000Z', 30, "ресторан", 2, '1 стол / до 4 человек'),
             (3, '2022-06-08T10:00:00.000Z', '2022-06-08T11:00:00.000Z', 130, "доставка", 3, 'NULL'),
             (4, '2022-03-08T10:00:00.000Z', '2022-03-08T11:00:00.000Z', 60, "доставка", 4, 'NULL'),
             (5, '2022-04-08T10:00:00.000Z', '2022-04-08T11:00:00.000Z', 70, "ресторан", 5, '1 стол / до 8 человек'),
             (6, '2022-05-08T10:00:00.000Z', '2022-05-08T11:00:00.000Z', 80, "ресторан", 6, '1 стол / до 4 человек')]

    with con:
        con.executemany(sql_insert, test5)

    # with con:
    #     data5 = con.execute("SELECT * FROM Orders")
    #     print(data5.fetchall())



except:
    print("Такой номер или telegram id уже занят")

con.execute