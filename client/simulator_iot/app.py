from wtforms.validators import InputRequired, ValidationError
from wtforms import StringField

from flask import Flask, render_template, json, request
from flask_wtf import FlaskForm

from datetime import datetime

import socket
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'


# Конвертер DATE в для передачи через JSON
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


# Общение с сервером
def broadcast(info):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    client_sock.connect(('127.0.0.1', 53210))

    b = json.dumps(info, default=date_handler).encode(
        'utf-8')  # Преобразование dict в str объект json, преобразовать этот str в bytes
    client_sock.sendall(b)  # Отправка словаря на сервер

    data = client_sock.recv(1024)

    # client_sock.close()

    return data


def validate_name(form, field):
    file = open('settings.sp')
    audience_name = str(file.read())
    date_now = datetime.now()

    info = {'barcode': [
        audience_name,
        date_now.strftime('%Y-%m-%d'),
        int(date_now.strftime('%H')),
        int(date_now.strftime('%M')),
        field.data
    ]}
    try:
        # TODO соединение к серверу и проверку валидность баркода
        access_successful = broadcast(info)
        if access_successful == b"None" or access_successful == b"[]":
            raise ValidationError("The entry does not exist.")
        else:
            if access_successful == b"True":
                raise ValidationError("Willkommen.")
            else:
                raise ValidationError("No access.")
    except Exception as ex:
        raise ValidationError(ex)


class LoginForm(FlaskForm):
    barcode = StringField('barcode', validators=[InputRequired(), validate_name])


@app.route('/', methods=['GET', 'POST'])
def main():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            return 'Form Successfully Submitted!'
    return render_template('index.html', form=form)


#@app.route('/', methods=['POST'])
#def test_barcode():
#    if request.method == 'POST':
#        print(request.form['barCode'])
#        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
