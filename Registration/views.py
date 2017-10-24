from django.shortcuts import render

def Registration(request):
    name = "Artem"
    return render(request, 'Registration/Registration.html', locals())