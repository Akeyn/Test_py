from datetime import date

import sqlite3
import socket
import json

import hashlib
import hmac

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('127.0.0.1', 53210))
serv_sock.listen(10)  # 10 - количество данных "в воздухе" которые попадут на сервер

client_sock, client_addr = serv_sock.accept()


def make_hash(value):
    MY_SECRET_KEY = b'T1F43cP0Rs821g'  # Ключ
    return hmac.new(key=MY_SECRET_KEY, msg=value.encode('utf-8'), digestmod=hashlib.sha224).hexdigest()


def processing(g_data):
    g_data = json.loads(g_data.decode('utf-8'))  # Декодирован из 'bytes' json обратно в DICT

    conn = sqlite3.connect('subscribers.db')  # Создание файла db
    c = conn.cursor()

    obr = list(g_data.keys())[0]  # Получение один из параметров (EXIST, SAVE, UPDATE, DELETE, LOGIN)
    value = g_data.get(obr)  # Получение имени таблицы[0], значений таблицы[1, ...N]

    if obr == 'save':
        # Заполнение таблицы пользователей
        if value[0] == 'registration_subscriber':
            c.execute('CREATE TABLE IF NOT EXISTS ' + value[
                0] + '(id INT, email TEXT, firstName TEXT, secondName TEXT, login TEXT, password TEXT, birthday DATE, country INT, created_at INT)')
            c.execute('INSERT INTO ' + value[0] + ' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                value[1],
                value[2],
                value[3],
                value[4],
                value[5],
                value[6],
                value[7],
                value[8],
                value[9],
            ))
        if value[0] == 'registration_historymeter':
            date_today = "2017-12-29"  # date.today()
            c.execute('CREATE TABLE IF NOT EXISTS ' + value[
                0] + '(meter_id INT, end_value REAL, difference REAL, currentdate DATE, start_value REAL)')

            c.execute("SELECT count(*) FROM " + value[0] + " WHERE meter_id = ?",
                      (value[1],))
            meter_history_exist = c.fetchone()

            c.execute("SELECT count(*) FROM " + value[0] + " WHERE meter_id = ? AND currentdate = ?",
                      (value[1], date_today,))
            meter_date_exist = c.fetchone()

            # Проверка на наличие истории
            if meter_history_exist[0] == 0:
                # Нет поля с таким id, то start_value = registration_meter.value WHERE meter_id = value[1], end_value = 0
                c.execute("SELECT value FROM registration_meter WHERE id = ?",
                          (value[1],))
                start_value_db = c.fetchone()

                start_value = start_value_db[0]
                end_value = value[2]
                print(0, start_value, end_value)  # TODO
            else:
                # Есть поле с таким id, то start_value = (Последняя строка с таким id).end_value, end_value = value[2]
                c.execute(
                    "SELECT end_value FROM registration_historymeter WHERE meter_id = ? ORDER BY currentdate DESC LIMIT 1",
                    (value[1],))
                end_value_db = c.fetchone()
                start_value = end_value_db[0]

                if end_value_db[0] != 0 and end_value_db[0] == value[2]:
                    start_value = value[2]

                end_value = value[2]
                print(1, start_value, end_value)  # TODO

            difference = end_value - start_value
            # Проверка на наличие поля c похожей датой в истории
            if meter_date_exist[0] == 0:
                if difference < 1:
                    difference = 0

                # Не существует поле с такой датой, то INSERT
                c.execute('INSERT INTO ' + value[0] + ' VALUES(?, ?, ?, ?, ?)', (
                    value[1],
                    end_value,
                    difference,
                    date_today,
                    start_value))
            else:
                # Существует поле с такой датой, то UPDATE
                c.execute("UPDATE " + value[0] + " SET end_value = ?, difference = ?, start_value = ? WHERE meter_id = ? AND currentdate = ?", (
                              end_value,
                              difference,
                              start_value,
                              value[1],
                              date_today,
                          ))

            print(meter_date_exist[0], meter_history_exist[0])  # TODO

    if obr == 'update':
        pass

    if obr == 'delete':
        pass

    if obr == 'login':
        # Проверка на существование пользователя
        try:
            c.execute("SELECT * FROM registration_subscriber WHERE login = ? AND password = ? ",
                      (value[0], make_hash(value[1]),))
            user_exist = c.fetchone() is not None

            if user_exist is True:
                client_sock.sendall(bytes(str(user_exist), "ascii"))
            else:
                client_sock.sendall(bytes(str(user_exist), "ascii"))
        except:
            print("error")

    conn.commit()
    c.close()
    conn.close()


if __name__ == '__main__':
    while True:  # Бесконечный цикл, пока сервер работает
        g_data = client_sock.recv(1024)  # Получение данных с клиента(размером 1MB)
        processing(g_data)
        client_sock.sendall(b'Your g_data: ' + g_data)  # Отправка данных клиенту
        if not g_data:  # Если данных нет выйти из цикла
            break