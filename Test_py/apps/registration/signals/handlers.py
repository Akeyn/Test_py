from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import *

import string
import socket
import json


# Конвертер DATE в для передачи через JSON
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


# Общение с сервером
def broadcast(info):
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        client_sock.connect(('127.0.0.1', 53210))

        b = json.dumps(info, default=date_handler).encode(
            'utf-8')  # Преобразование dict в str объект json, преобразовать этот str в bytes
        client_sock.sendall(b)  # Отправка словаря на сервер

        data = client_sock.recv(1024)

        client_sock.close()

        print(' - - -> ', repr(data))
    except:
        print(' -- ERROR CONNECTION -- ')


def send_data(type_of_send, fields):  # Словарь для отправки на сервер
    info = {type_of_send: fields}
    broadcast(info)


@receiver(post_save, sender=Lecturer)
def save_lecturer(instance, created, **kwargs):
    lecturer = instance
    type_of_send = 'save' if created else 'update'
    send_data(type_of_send, [
        'registration_lecturer',
        lecturer.id,
        lecturer.email,
        lecturer.firstName,
        lecturer.secondName,
        lecturer.login,
        lecturer.password,
        lecturer.birthday,
        lecturer.country,
        lecturer.created_at,
        str(lecturer.rfid)
    ])


@receiver(post_save, sender=Audience)
def save_audience(instance, created, **kwargs):
    audience = instance
    type_of_send = 'save' if created else 'update'
    send_data(type_of_send, [
        'registration_audience',
        audience.id,
        audience.audience_name
    ])


@receiver(post_save, sender=Schedule)
def save_schedule(instance, created, **kwargs):
    schedule = instance
    type_of_send = 'save' if created else 'update'
    send_data(type_of_send, [
        'registration_schedule',
        schedule.id,
        schedule.lecture,
        schedule.audience_name,
        schedule.day,
        schedule.lecturer,
        schedule.is_passed
    ])

@receiver(post_delete, sender=Audience)
def delete_audience(instance, **kwargs):
    audience = instance
    send_data('delete', [
        'registration_audience',
        audience.id
    ])


@receiver(post_delete, sender=Lecturer)
def delete_lecturer(instance, **kwargs):
    lecturer = instance
    send_data('delete', [
        'registration_lecturer',
        lecturer.id,
    ])


@receiver(post_delete, sender=Schedule)
def delete_schedule(instance, **kwargs):
    schedule = instance
    send_data('delete', [
        'registration_schedule',
        schedule.id,
    ])
