from django.contrib.auth.forms import UserCreationForm


from UserProfile.models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'phone', 'age', 'address', 'email', 'password1', 'password2')