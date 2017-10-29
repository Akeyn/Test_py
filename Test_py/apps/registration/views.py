from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *

# Create your views here.


def registration(request):

    form = RegistrationForm(data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return render(request, 'registration.html', locals())
        else:
            return render(request, 'registration.html', locals())

    else:
        form = RegistrationForm()

        context = {'form': form}

        return render(request, 'registration.html', context)

def login(request):

    form = LoginForm(data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            print('1')  # Text
            return render(request, 'login.html', locals())
        else:
            print('invalid')  # Text
            return render(request, 'login.html', locals())

    else:
        form = LoginForm()
        print('Dont POST')  # Text

        context = {'form': form}

        return render(request, 'login.html', context)
"""
countries = Country.objects.all()

context = {'countries': countries}

return render(request, 'registration.html', context)
"""

def error(request):
    return render(request, 'Error.html')

"""
def registration_user(request):

    form = RegistrationForm(data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            print('1')
            return render(request, 'Registration.html', locals())
            # form.save()
            # return render(request, 'Registration.html', locals())
        else:
            print('invalid')
            return render(request, 'Registration.html', locals())

    else:
        form = RegistrationForm()
        print('Dont POST')
        context = {'form': form}

        return render(request, 'Registration.html', context)
"""

"""
email = request.POST.get('email')
firstname = request.POST.get('firstname')
secondname = request.POST.get('secondname')
login = request.POST.get('login')
password = request.POST.get('password')
confirmPassword = request.POST.get('confirmPassword')
date = request.POST.get('date')
country = request.POST.get('country')
checkbox = request.POST.get('checkbox', False)
"""

"""
def re(request, index):

    try:
        re = Country.objects.get(country_id=index)
        result = re.country_name
    except Country.DoesNotExist:
        result = "Does not exist"

    return HttpResponse(result)
"""