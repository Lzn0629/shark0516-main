from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
import re

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'sex')
        widgets = {
            'password1':forms.PasswordInput(),
            'password2':forms.PasswordInput(),
        }
        labels = {
            'username':'手機號',
            'password1':'密碼',
            'password2':'密碼確認',
            'first_name':'姓名',
            'sex':'性別',
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('請輸入電子郵件')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('請輸入手機號')
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError('該手機號已註冊')
        elif not re.match(r'09\d{8}', username):
            raise forms.ValidationError('請輸入09開頭的正確手機號')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('請輸入姓名')
        return first_name

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("兩次輸入的密碼不匹配")
        return cleaned_data

class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ['numberOfPeople', 'date', 'time', 'note']
        widgets = {
            'date':forms.DateInput(),
        }
        labels = {
            'numberOfPeople': '人數',
            'date':'日期',
            'time':'時段',
            'note':'備註',
        }

class ReserveSearchForm(forms.Form):
    time = forms.ModelChoiceField(queryset=Time.objects.all(), required=False)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'price', 'introduce', 'allergy', 'image', 'listingDate',
                   'isVegetarian', 'classification']
        widgets = {
            'image' : forms.FileInput(attrs={'class': 'form-control-file'}),
            'listingDate':forms.DateInput()
        }
        labels = {
            'name':'餐點名稱',
            'price':'價錢',
            'introduce':'餐點介紹',
            'allergy':'餐點成分',
            'image':'餐點圖片',
            'listingDate':'上架日期',
            'isVegetarian':'素食可用',
            'classification':'餐點分類'
        }

class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['name', 'timeStart', 'timeEnd', 'numberOfPeopleMax']
        labels = {
            'name':'時段名稱',
            'timeStart':'起始時間',
            'timeEnd':'終止時間',
            'numberOfPeopleMax':'時段預約人數上限'   
        }

class ClassificationForm(forms.ModelForm):
    class Meta:
        model = Classification
        fields = '__all__'
        labels={
            'name':'分類名稱'
        }