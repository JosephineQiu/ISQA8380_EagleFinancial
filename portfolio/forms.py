from django import forms
from .models import *
from django.contrib.auth.models import User


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cust_number', 'name', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone')



class StockForm(forms.ModelForm):
   class Meta:
       model = Stock
       fields = ('customer', 'symbol', 'name', 'shares', 'purchase_price', 'purchase_date',)



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Sorry, the passwords don\'t match. Please try again.')
        return cd['password2']


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ('customer','category','description','cost_basis','recent_value','recent_date')

