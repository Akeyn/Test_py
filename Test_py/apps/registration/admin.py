from django.contrib import admin
from django import forms
from .models import *
from .forms import *

# Register your models here.


class AudienceForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ['audience_name']

    def clean(self):
        audience_name = self.cleaned_data.get('audience_name')
        is_exist_audience_name = Audience.objects.filter(audience_name=audience_name).first()
        if is_exist_audience_name:
            raise forms.ValidationError("Audience name is already exist.")
        return self.cleaned_data


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [
            'lecture',
            'audience_name',
            'day',
            'lecturer',
        ]

    def clean(self):
        lecture = self.cleaned_data.get('lecture')
        audience_name = self.cleaned_data.get('audience_name')
        day = self.cleaned_data.get('day')
        lecturer = self.cleaned_data.get('lecturer')

        is_busy_lecturer = Schedule.objects.filter(
            lecturer=lecturer,
            day=day,
            audience_name=audience_name,
            lecture=lecture).first()
        is_busy_lecturer2 = Schedule.objects.filter(
            lecturer=lecturer,
            day=day,
            lecture=lecture).first()
        is_busy_audience = Schedule.objects.filter(
            day=day,
            audience_name=audience_name,
            lecture=lecture).first()

        if is_busy_lecturer or is_busy_lecturer2:
            raise forms.ValidationError("Lecturer is busy.")
        if is_busy_audience:
            raise forms.ValidationError("Audience is busy.")
        return self.cleaned_data


class AudienceAdmin(admin.ModelAdmin):
    form = AudienceForm
    list_display = (
        'id',
        'audience_name',
    )


class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleForm
    list_display = (
        'id',
        'lecture',
        'audience_name',
        'day',
        'lecturer',
    )


class LecturerAdmin(admin.ModelAdmin):
    form = RegistrationForm
    list_display = (
        'id',
        'email',
        'firstName',
        'secondName',
        'login',
        'password',
        'birthday',
        'country',
        'picture',
    )
    fields = [
        'email',
        'firstName',
        'secondName',
        'login',
        'password',
        'confirmPassword',
        'birthday',
        'country',
        'picture',
        'checkbox'
    ]


admin.site.register(Lecturer)  # LecturerAdmin
admin.site.register(Audience, AudienceAdmin)
admin.site.register(Schedule, ScheduleAdmin)
# admin.site.register(Country)
# admin.site.register(TypeMeter)
# admin.site.register(Meter)
# admin.site.register(HistoryMeter)
