from django import forms
from .models import *
from django.forms import BaseForm

# Create your forms here.


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseForm, self).__init__(*args, **kwargs)

class BaseModelForm(forms.ModelForm):
    """
    Delete label_suffix ':'
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseModelForm, self).__init__(*args, **kwargs)

class RegistrationForm(BaseModelForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'password'}))
    checkbox = forms.BooleanField(widget=forms.CheckboxInput(attrs={}), label='You have read and agree with terms and conditions of the <a href="#">AVM Customer Agreement</a>')

    class Meta:
        # exclude = ['email', 'firstName'] # Исключить поля из модели Subscriber
        model = Subscriber

        fields = [
            'email',
            'firstName',
            'secondName',
            'login',
            'password',
            'confirmPassword',
            'date',
            'country',
        ]

        """
        error_messages = {
            'password': {
                "invalid": ("Passwords don't match"),
            },
        }
        """

        # widgets = {'date': forms.SelectDateWidget()} # Виджет для дыты
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'firstName': forms.TextInput(attrs={'placeholder': 'firstName'}),
            'secondName': forms.TextInput(attrs={'placeholder': 'secondName'}),
            'login': forms.TextInput(attrs={'placeholder': 'login'}),
            'password': forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'password'}),
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'date'}),
        }

    def clean(self):
        Subscriber.password = self.cleaned_data.get('password', None)
        confirmPassword = self.cleaned_data.get('confirmPassword', None)
        # checkbox = self.cleaned_data.get('checkbox', False)

        if Subscriber.password and confirmPassword and (Subscriber.password == confirmPassword):
            return self.cleaned_data
        else:
            # self._errors["confirmPassword"] = self.error_class(["Passwords don't match"])
            self.add_error('password', '')
            self.add_error('confirmPassword', "Passwords don't match")
            raise forms.ValidationError("Passwords don't match")

class LoginForm(BaseForm):
    loginEmail = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Email or login'}), label='Email or login')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'password'}), label='Password')

    # Delete field 'checkbox'
    """
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['checkbox']
    """



    """
    def save(self, commit=True):
        Subscriber.password = self.cleaned_data.get('password', None)
        Subscriber.email = self.cleaned_data.get('email', None)
        Subscriber.firstname = self.cleaned_data.get('firstname', None)
        Subscriber.secondname = self.cleaned_data.get('secondname', None)
        Subscriber.login = self.cleaned_data.get('login', None)
        Subscriber.date = self.cleaned_data.get('date', None)
        Subscriber.country = self.cleaned_data.get('country', None)

        if commit:
            Subscriber.save()

        return Subscriber
    """