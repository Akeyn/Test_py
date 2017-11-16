from datetime import datetime, date, time, timedelta
from Test_py.modules.digester import make_hash

from django.forms import BaseForm
from django.db.models import Q
from django import forms
from .models import *

import string
import socket
import json
import re

# Create your forms here.


# Конвертер DATE в для передачи через JSON
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


# Общение с сервером
def broadcast(info):
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        client_sock.connect(('127.0.0.1', 53210))

        b = json.dumps(info, default=date_handler).encode('utf-8')  # Преобразование dict в str объект json, преобразовать этот str в bytes
        client_sock.sendall(b)  # Отправка словаря на сервер

        data = client_sock.recv(1024)

        client_sock.close()

        print(' - - -> ', repr(data))
    except:
        print(' -- ERROR CONNECTION -- ')


# Метод проверки на кириллицу
def kirillic(err, name, str_name):
    if re.search(r"[А-Яа-я]", name):
        return err.setdefault("Invalid format!", []).append({
            str_name: "Cyrillic characters can't be used in password!"})

# Метод проверка на знаки \W, без пробельных знаков \s (first name, second name)
def no_char(err, name, str_name):
    name = name.strip()
    name = re.sub('\s', '', str(name))

    if re.findall('[\W\d_]', name):
        return err.setdefault("Field must contain only characters!", []).append({
            str_name: "Field must contain only characters!"})


# Метод проверка пробелов в полях
def cln(err, name, str_name):
    name = name.strip()

    if re.sub('\s', '', str(name)) != name:
        return err.setdefault("Field shouldn't contain emptiness!", []).append({
            str_name: "Field shouldn't contain emptiness!"})


# Метод проверка длины поля
def length_check(err, name, str_name):
    if len(name) <= 2:
        return err.setdefault("Field must contain at least 3 characters!", []).append({
            str_name: "Field must contain at least 3 characters!"})


# Метод проверки массива ошибок
def error_existence(self, err):
    if err:
        for ERROR_MSG in err.keys():
            for LIST_FIELDS in err.get(ERROR_MSG):
                for i in LIST_FIELDS:
                    self.add_error(i, LIST_FIELDS[i])  # For Example: ('email', "Email already exists")

        # Вызов лист ключей из словаря
        raise forms.ValidationError(list(err))
    else:
        return self.cleaned_data


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseForm, self).__init__(*args, **kwargs)


# Delete label_suffix ':'
class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseModelForm, self).__init__(*args, **kwargs)


class RegistrationForm(BaseModelForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'password'}))
    checkbox = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label='You have read and agree with terms and conditions of the <a href="#">AVM Customer Agreement</a>')

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['secondName'].required = False
        self.fields['country'].required = False
        self.fields['birthday'].required = False

    class Meta:
        model = Subscriber
        fields = [
            'email',
            'firstName',
            'secondName',
            'login',
            'password',
            'confirmPassword',
            'birthday',
            'country',
        ]
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'firstName': forms.TextInput(attrs={'placeholder': 'firstName'}),
            'secondName': forms.TextInput(attrs={'placeholder': 'secondName'}),
            'login': forms.TextInput(attrs={'placeholder': 'login'}),
            'password': forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'password'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'placeholder': 'birthday',
                                               'max': datetime.now().strftime('%Y-%m-%d'),
                                               'min': (datetime.now()-timedelta(days=365*100)).strftime('%Y-%m-%d'),
                                               'onkeydown': 'return false',
                                               }),
        }

    def clean(self):
        # Словарь ключей ошибок, со списком словарей [{"имя_поля_1": "ошибка_поля_1", "имя_поля_2": "ошибка_поля_2"}, ]
        errors = {}

        c_email = self.cleaned_data.get('email', None)
        c_first_name = self.cleaned_data.get('firstName', None)
        c_second_name = self.cleaned_data.get('secondName', None)
        c_login = self.cleaned_data.get('login', None)
        c_password = self.cleaned_data.get('password', None)
        c_confirm_password = self.cleaned_data.get('confirmPassword', None)

        email = Subscriber.objects.filter(email=c_email).first()
        login = Subscriber.objects.filter(login=c_login).first()

        # Проверка на кириллицу
        kirillic(errors, c_login, "login")
        kirillic(errors, c_first_name, "firstName")
        kirillic(errors, c_second_name, "secondName")
        kirillic(errors, c_password, "confirmPassword")

        # Проверка длины полей
        length_check(errors, c_login, "login")
        length_check(errors, c_first_name, "firstName")
        length_check(errors, c_second_name, "secondName")

        # Проверка пустоты полей
        cln(errors, c_login, "login")
        cln(errors, c_first_name, "firstName")
        cln(errors, c_second_name, "secondName")

        # Проверка логина на знаки \W, без пробельных знаков \s
        c_login = c_login.strip()
        c_login = re.sub('\s', '', str(c_login))
        if re.findall('[\W]', c_login):
            return errors.setdefault("Field must contain only characters and numbers!", []).append(
                {"login": "Field must contain only characters and numbers!"})

        # Проверка на знаки \W\d, без пробельных знаков \s
        no_char(errors, c_first_name, "firstName")
        no_char(errors, c_second_name, "secondName")

        # Валидация Email
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        try:
            if not re.match(email_regex, c_email):
                errors.setdefault("Invalid email format!", []).append({"email": "Invalid email format!"})
        except:
            errors.setdefault("Invalid email format!", []).append({"email": "Invalid email format!"})

        # Проверка на существование Email
        if email is not None:
            errors.setdefault("Email already exists!", []).append({"email": "Email already exists!"})

        # Проверка на существование Login
        if login is not None:
            errors.setdefault("Login already exists!", []).append({"login": "Login already exists!"})

        # Проверка есть ли в пароле lowercase "а"
        if not re.search(r"[a-z]", c_password):
            errors.setdefault("Invalid password format!", []).append({
                "password": "",
                "confirmPassword": "Password must contain at least 1 letter in lowercase!",
            })
        else:
            # Проверка есть ли в пароле uppercase "А"
            if not re.search(r"[A-Z]", c_password):
                errors.setdefault("Invalid password format!", []).append({
                    "password": "",
                    "confirmPassword": "Password must contain at least 1 letter in uppercase!",
                })
            else:
                # Проверка есть ли в пароле "number"
                if not re.search(r"[0-9]", c_password):
                    errors.setdefault("Invalid password format!", []).append({
                        "password": "",
                        "confirmPassword": "Password must contain at least 1 number!",
                    })

        # Проверка длины пароля
        if len(c_password) <= 5:
            errors.setdefault("Invalid password format!", []).append({
                "password": "",
                "confirmPassword": "Field must contain at least 6 characters!",
            })
        else:
            # Проверка схожести паролей
            if not (c_password and c_confirm_password and (c_password == c_confirm_password)):
                errors.setdefault("Passwords don't match!", []).append({
                    "password": "",
                    "confirmPassword": "Passwords don't match!"})

        # Вызов метода проверки массива ошибок
        error_existence(self, errors)

    # Сохранение данных в бд
    def save(self, commit=False):
        # Изменение данных перед отправкой
        subscriber, created = Subscriber.objects.update_or_create(
            password=make_hash(self.cleaned_data.get('password', None)),
            email=self.cleaned_data.get('email', None),
            firstName=self.cleaned_data.get('firstName', None),
            secondName=self.cleaned_data.get('secondName', None),
            login=self.cleaned_data.get('login', None),
            birthday=self.cleaned_data.get('birthday', None),
            country=self.cleaned_data.get('country', None)
        )
        info = {'save': [
            'registration_subscriber',
            subscriber.id,
            subscriber.email,
            subscriber.firstName,
            subscriber.secondName,
            subscriber.login,
            subscriber.password,
            subscriber.birthday,
            subscriber.country,
            subscriber.created_at
            ]}  # Словарь для отправки на сервер
        broadcast(info)  # Отправка данных на сервер
        return subscriber


class LoginForm(BaseForm):
    loginEmail = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Email or login'}),
                                 label='Email or login')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'password'}),
                               label='Password')

    def clean(self):
        # Словарь ключей ошибок, со списком словарей [{"имя_поля_1": "ошибка_поля_1", "имя_поля_2": "ошибка_поля_2"}, ]
        errors = {}

        c_login_email = self.cleaned_data.get('loginEmail', None)
        c_password = self.cleaned_data.get('password', None)
        sub = Subscriber

        # Создания хэша пароля с формы если он был введен
        if c_password is not None:
            c_password = make_hash(self.cleaned_data.get('password'))  # Make_hash

        # Запрос на получение user по email или login
        user_login_email = sub.objects.filter(login=c_login_email).first() or sub.objects.filter(
            email=c_login_email).first()

        # Получения по запросу usr pass
        user_password = sub.objects.filter(password=c_password, login=c_login_email).first() or sub.objects.filter(
            password=c_password, email=c_login_email).first()

        # Проверка login или Email, есть или нет в бд
        if user_login_email is None:
            errors.setdefault("Login or Email doesn't exist", []).append({"password": "", "loginEmail": ""})
        else:
            # Проверка пароля
            if c_password is not None and user_password is None:
                errors.setdefault("Incorrect password", []).append({"password": ""})

        # Вызов метода проверки массива ошибок
        error_existence(self, errors)

    # Метод проверки массива ошибок
    """
    def error_existence(self, err):
        if err:
            for key in err.keys():
                for error in err.get(key):
                    self.add_error(error, err.get(key)[error])  # For Example: ('email', "Email already exists")

            raise forms.ValidationError(list(err))
        else:
            return self.cleaned_data
    """

    # Delete field 'checkbox'
    """
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['checkbox']
    """

    #  errors.setdefault("Email already exists", {"email": "Email already exists"})
    #  errors.setdefault("Login already exists", {"login": "Login already exists"})
    #  errors.setdefault("Passwords don't match", {"password": "", "confirmPassword": "Passwords don't match"})
    #  errors.setdefault("Login or Email doesn't exist", {"password": "", "loginEmail": ""})
    #  errors.setdefault("Incorrect password", {"password": ""})
