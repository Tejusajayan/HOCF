from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
class userform(UserCreationForm):
    email=forms.EmailField()
    class meta:
        model=User
        fields=['username','email','password1','password2','is_active']

class shippdet(forms.Form):
    name = forms.CharField(max_length=100)
    number = forms.CharField(max_length=15)
    doorno_street_area = forms.CharField(max_length=200)
    landmark = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=6)