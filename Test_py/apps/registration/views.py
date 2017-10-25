from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def registration(request):

    #return HttpResponse("Hi!")
    return render(request, 'Registration.html', locals())