from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  #djnago built-in User Model
from django import forms
from django.forms.widgets import PasswordInput, TextInput # for login input

#Registraion Form

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
    def __init__(self, *args, **kwargs):
        
        super(CreateUserForm, self).__init__(*args, **kwargs)

        # Hide help text for password fields (but keep validation)
        # self.fields['username'].help_text = None
        self.fields['email'].required = True  #email field required 
        self.fields['password1'].help_text = None
        # self.fields['password2'].help_text = None

    #Email Validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email already exists')
        
        if len(email) >= 300 :
            raise forms.ValidationError('Your Email is Too Long')
        
        return email
    


# Login Form ##

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



# Update Form

class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude =  ['password1', 'password2'] # Don't Want These Fields

    def __init__(self, *args, **kwargs):

        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True  #email field required 

    # Update Email Validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email already exists')
        
        if len(email) >= 300 :
            raise forms.ValidationError('Your Email is Too Long')
        
        return email


