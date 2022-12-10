from django import forms
from blogApp.models import *
from django.contrib.auth.models import User

import time
class SignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','password','email','first_name','last_name')

class PostMail(forms.Form):
    Name=forms.CharField(max_length=30)
    Email=forms.EmailField()
    Password=forms.CharField(max_length=30)
    To=forms.EmailField()
    comments=forms.CharField(widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=('name','mail','body')

    '''name=forms.CharField(max_length=30)
    mail=forms.EmailField()
    body=forms.CharField(widget=forms.Textarea)'''

class OtpForm(forms.Form):
    Otp=forms.IntegerField()
    
