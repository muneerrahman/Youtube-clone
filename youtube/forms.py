from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Your name', max_length=20)
    password = forms.CharField(label='password', max_length=20)
class RegisterForm(forms.Form):
    username = forms.CharField(label='Your name', max_length=20)
    password = forms.CharField(label='password', max_length=20)
    email = forms.CharField(label='email', max_length=20)
class NewVideoForm(forms.Form):
    title = forms.CharField(label='TITLE', max_length=20)
    description = forms.CharField(label='description', max_length=20)
    file = forms.FileField()

class CommentForm(forms.Form):
    text = forms.CharField(label='text', max_length=300)
    # video=forms.HiddenInput()
    user=forms.IntegerField(widget=forms.HiddenInput(),initial=1)