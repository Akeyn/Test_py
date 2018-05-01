from datetime import date

import sqlite3
import socket
import json

import hashlib
import hmac

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('127.0.0.1', 53210))
serv_sock.listen(10)  # 10 - количество данных "в воздухе" которые попадут на сервер


def make_hash(value):
    MY_SECRET_KEY = b'T1F43cP0Rs821g'  # Ключ
    return hmac.new(key=MY_SECRET_KEY, msg=value.encode('utf-8'), digestmod=hashlib.sha224).hexdigest()


def processing(g_data):
    g_data = dict(json.loads(g_data.decode('utf-8')))  # Декодирован из 'bytes' json обратно в DICT

    conn = sqlite3.connect('lecturers.db')  # Создание файла db
    c = conn.cursor()

    obr = list(g_data.keys())[0]  # Получение один из параметров (EXIST, SAVE, UPDATE, DELETE, LOGIN)
    value = g_data.get(obr)  # Получение имени таблицы[0], значений таблицы[1, ...N]

    try:
        if obr == 'save':
            # Заполнение таблицы пользователей
            if value[0] == 'registration_lecturer':
                c.execute('CREATE TABLE IF NOT EXISTS ' + value[0] + '(id INT, email TEXT, firstName TEXT, secondName TEXT, login TEXT, password TEXT, birthday DATE, country INT, created_at INT, rfid TEXT)')
                c.execute('INSERT INTO ' + value[0] + ' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                    value[1],
                    value[2],
                    value[3],
                    value[4],
                    value[5],
                    value[6],
                    value[7],
                    value[8],
                    value[9],
                    value[10],
                ))
            # Заполнение таблицы аудиторий
            if value[0] == 'registration_audience':
                c.execute('CREATE TABLE IF NOT EXISTS ' + value[0] + '(id INT, audience_name INT)')
                c.execute('INSERT INTO ' + value[0] + ' VALUES(?, ?)', (
                    value[1],
                    value[2],
                ))
            # Заполнение таблицы расписание
            if value[0] == 'registration_schedule':
                c.execute('CREATE TABLE IF NOT EXISTS ' + value[0] + '(id INT, lecture INT, audience_name INT, day DATE, lecturer TEXT, is_passed INT)')
                c.execute('INSERT INTO ' + value[0] + ' VALUES(?, ?, ?, ?, ?, ?)', (
                    value[1],
                    value[2],
                    value[3],
                    value[4],
                    value[5],
                    value[6],
                ))

        if obr == 'update':
            if value[0] == 'registration_lecturer':
                c.execute('UPDATE registration_lecturer SET email = ?, firstName = ?, secondName = ?, login = ?, password = ?, birthday = ?, country = ? WHERE id = ?', (
                    value[2],
                    value[3],
                    value[4],
                    value[5],
                    value[6],
                    value[7],
                    value[8],
                    value[1],
                ))
            # Заполнение таблицы аудиторий
            if value[0] == 'registration_audience':
                c.execute('UPDATE registration_audience SET audience_name = ? WHERE id = ?', (
                    value[2],
                    value[1],
                ))
            if value[0] == 'registration_schedule':
                c.execute('UPDATE registration_schedule SET lecture = ?, audience_name = ?, day = ?, lecturer = ? WHERE id = ?', (
                    value[2],
                    value[3],
                    value[4],
                    value[5],
                    value[1],
                ))

        if obr == 'delete':
            # Удаление таблицы пользователей
            if value[0] == 'registration_lecturer':
                c.execute("DELETE FROM registration_lecturer WHERE id = ? ",
                          (value[1],))
            # Удаление таблицы аудиторий
            if value[0] == 'registration_audience':
                c.execute("DELETE FROM registration_audience WHERE id = ? ",
                          (value[1],))
            # Удаление таблицы расписание
            if value[0] == 'registration_schedule':
                c.execute("DELETE FROM registration_schedule WHERE id = ? ",
                          (value[1],))

        if obr == 'login':
            # Проверка на существование пользователя
            try:
                c.execute("SELECT * FROM registration_lecturer WHERE login = ? AND password = ? ",
                          (value[0], make_hash(value[1]),))
                user_exist = c.fetchone() is not None

                if user_exist is True:
                    client_sock.sendall(bytes(str(user_exist), "ascii"))
                else:
                    client_sock.sendall(bytes(str(user_exist), "ascii"))
            except:
                print("error")
    except:
        pass

    conn.commit()
    c.close()
    conn.close()


if __name__ == '__main__':
    while True:  # Бесконечный цикл, пока сервер работает
        client_sock, client_addr = serv_sock.accept()
        g_data = client_sock.recv(1024)  # Получение данных с клиента(размером 1MB)
        if g_data != b'':
            processing(g_data)
            client_sock.sendall(b'Your g_data: ' + g_data)  # Отправка данных клиенту
        #else:  # Если данных нет выйти из цикла
        #    break
