from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from captcha.fields import ReCaptchaField

class ExtendedPasswordResetForm(PasswordResetForm):

    class Meta:
        model = get_user_model()

    captcha = ReCaptchaField()

class ExtendedUserCreationForm(UserCreationForm):
    '''Add recaptcha and timezone to the standard creation form.'''

    class Meta:
        model = get_user_model()        
        fields = ['username', 'email', 'password1', 'password2', 'captcha']

    captcha = ReCaptchaField()
