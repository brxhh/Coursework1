from .models import Story
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, login

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердження паролю', widget=forms.PasswordInput)
    email = forms.EmailField(label='Електронна пошта', required=False, help_text="Необов'язково")

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Паролі не співпадають.')
        return cd['password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def login_user(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content', 'author', 'likes', 'is_read']