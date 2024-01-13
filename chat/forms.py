from django import forms

class Register_form(forms.Form):
    Username = forms.CharField(label="Username",min_length=3,max_length=30,required=True,
    widget=forms.TextInput(attrs={'style': 'width: 500px;', 'class': 'form-control'}))


    Password = forms.CharField(label="Password",min_length=8,required=True,
    widget=forms.TextInput(attrs={'style': 'width: 500px;', 'class': 'form-control'}))

    ConfirmPassword = forms.CharField(label="Confirm Password",required=True,
    widget=forms.TextInput(attrs={'style': 'width: 500px;', 'class': 'form-control'}))

class Login_form(forms.Form):
    Username = forms.CharField(label="Username",required=True,
    widget=forms.TextInput(attrs={'style': 'width: 500px;', 'class': 'form-control'}))
    Password = forms.CharField(label="Password",required=True,
    widget=forms.TextInput(attrs={'style': 'width: 500px;', 'class': 'form-control'}))
