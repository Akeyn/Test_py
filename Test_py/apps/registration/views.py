from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *

# Create your views here.


def handle_uploaded_file(f):
    with open('/images/data.png', 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)


def registration(request):
    form = RegistrationForm(request.POST, request.FILES or None)

    if request.method == "POST":
        login = request.POST.get('login', None)

        if form.is_valid() and request.session.get("user_id") is None:  # Проверка формы is_valid и существования сессии
            form.save()
            user = Subscriber.objects.filter(login=login).first()  # Получение логина пользователя
            request.session['user_id'] = str(user.id)  # Сделать создание сессии не тут
            return redirect('/Userpage')  # Перенаправление на страницу пользователя
        else:
            return render(request, 'registration.html', locals())
    else:
        form = RegistrationForm()
        context = {'form': form}

        return render(request, 'registration.html', context)


def login(request):
    form = LoginForm(request.POST, request.FILES)

    if request.method == "POST":
        loginEmail = request.POST.get('loginEmail', None)

        if form.is_valid() and request.session.get("user_id") is None:  # Проверка формы is_valid и существования сессии
            user = Subscriber.objects.filter(login=loginEmail).first() or Subscriber.objects.filter(
                email=loginEmail).first()  # Получение логина или почты пользователя
            request.session['user_id'] = str(user.id)  # Сделать создание сессии не тут

            return redirect('/Userpage')  # Перенаправление на страницу пользователя
        else:
            return render(request, 'login.html', locals())

    else:
        #del request.session['user_id']  # Удаление сессии
        form = LoginForm()
        context = {'form': form}

        return render(request, 'login.html', context)


def userpage(request):
    if request.method == "POST":
        logout = request.POST.get('logout', None)

        if logout and request.session['user_id']:
            del request.session['user_id']  # Удаление сессии
            return redirect('/')  # Переадресация на главную страницу

    try:
        return render(request, 'userpage.html', {'Subscriber': Subscriber.objects.get(id=request.session['user_id'])})
    except:
        return render(request, 'userpage.html')


def editinfo(request):
    usr = request.session['user_id']
    sub = Subscriber.objects.get(id=usr)

    form = EditForm(usr, request.POST, request.FILES)

    if request.method == "POST":
        if form.is_valid():
            form = Subscriber.objects.get(id=usr)
            form.firstName = request.POST.get('firstName', None)
            form.secondName = request.POST.get('secondName', None)
            form.birthday = request.POST.get('birthday', None)
            if request.FILES.get('picture', None) is not None:
                form.picture = request.FILES.get('picture', None)
            form.save()

            return redirect('/Userpage/Edit')
        else:
            return render(request, 'editinfo.html', locals())
    else:
        form = EditForm(usr)
        context = {'form': form, 'Subscriber': sub}

        return render(request, 'editinfo.html', context)


def userlist(request):
    return render(request, 'userlist.html', {'Subscribers': Subscriber.objects.all()})


def error(request):
    return render(request, 'Error.html')


def test(request):
    return render(request, 'Test.html')

# m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")

"""
def re(request, index):

    try:
        re = Country.objects.get(country_id=index)
        result = re.country_name
    except Country.DoesNotExist:
        result = "Does not exist"

    return HttpResponse(result)
"""