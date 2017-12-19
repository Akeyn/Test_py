import socket
import json

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
client_sock.connect(('127.0.0.1', 53210))

file = open('value.sp')
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
