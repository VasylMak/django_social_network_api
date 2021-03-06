from django import forms

from posts.models import Post


# User registration custom form
class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'})
    )


# New post model form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']