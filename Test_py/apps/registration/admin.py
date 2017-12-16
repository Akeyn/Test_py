from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Country)
admin.site.register(Subscriber)
admin.site.register(TypeMeter)
admin.site.register(Meter)
admin.site.register(HistoryMeter)