from flask import render_template
from flask import Flask

import jinja2

import socket
import json

app = Flask(__name__)

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('/templates'),
])

app.jinja_loader = my_loader

"""
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
client_sock.connect(('127.0.0.1', 53210))

file = open('identifier.sp')
id = 18
value = float(file.read())

info = {'save': [
    'registration_historymeter',
    id,
    value,
]}  # Словарь для отправки на сервер

b = json.dumps(info).encode(
    'utf-8')  # Преобразование dict в str объект json, преобразовать этот str в bytes
client_sock.sendall(b)  # Отправка словаря на сервер

data = client_sock.recv(1024)

client_sock.close()

print(' - - -> ', repr(data))
"""


@app.route('/')
def hello_world():
    return render_template('barcodereader.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
