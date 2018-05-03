import kivy
kivy.require('1.9.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

import os
import socket
import json

from connected import Connected


# Конвертер DATE в для передачи через JSON
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def broadcast(info):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    client_sock.connect(('127.0.0.1', 53210))

    b = json.dumps(info, default=date_handler).encode(
        'utf-8')  # Преобразование dict в str объект json, преобразовать этот str в bytes
    client_sock.sendall(b)  # Отправка словаря на сервер

    data = client_sock.recv(1024)

    # client_sock.close()

    return data


def exception_handler(ex):
    ex = str(ex)
    box = FloatLayout()

    lbl = Label(text=ex, font_size=15, size_hint=(None, None),
                pos_hint={'center_x': 0.5, 'center_y': 0.6})
    box.add_widget(lbl)

    btn = Button(text='Close', size_hint=(None, None), width=454, height=50, pos_hint={'x': 0, 'y': 0})
    box.add_widget(btn)

    popup = Popup(title=ex, content=box, size_hint=(None, None), size=(480, 400), auto_dismiss=False)
    btn.bind(on_press=popup.dismiss)

    popup.open()


class Main(Screen):  # TODO
    pass


class MainApp(App):  # TODO
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Main(name='Main'))

        return manager


class Login(Screen):
    def my_func(self, login_text, password_text):
        info = {'login': [
            login_text,
            password_text,
        ]}  # Словарь для отправки на сервер

        try:
            user_exist = broadcast(info)

            if user_exist == b"True":
                self.processing_login(login_text, password_text)
            else:
                exception_handler("User doesn't exist")
        except Exception as ex:
            exception_handler(ex)

    def processing_login(self, login_text, password_text):
        app = App.get_running_app()

        app.username = login_text
        app.password = password_text

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()

    def reset_form(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""


class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))

        return manager


if __name__ == '__main__':
    # MainApp().run()  # TODO
    LoginApp().run()
    # MyApp().run()
