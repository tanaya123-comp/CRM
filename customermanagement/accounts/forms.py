from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models  import User

class orderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ('customer','product','status')

class customerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=('user',)

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email','password1','password2')

#revati chinmaymadhav
#tanaya tanaya
#parth krisha@123



