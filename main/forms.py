from allauth.account.forms import SignupForm
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django import forms



class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')

        if not name:
            raise forms.ValidationError("Please enter your name.")

        if not email:
            raise forms.ValidationError("Please enter your email address.")

        if not message:
            raise forms.ValidationError("Please enter a message.")
        
        return cleaned_data
    

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
 
    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        self.cleaned_data = self.clean()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        user.save()
        return user