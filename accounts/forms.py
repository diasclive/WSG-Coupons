from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from django import forms

from .models import Person

class PersonCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kwargs):
        super(PersonCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Person
        fields = ("username","first_name","last_name","date_of_birth","anniversary","phone_number","email",)


class PersonChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kwargs):
        super(PersonChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Person
        fields = '__all__'

class EditProfileForm(forms.ModelForm):
   
    class Meta:
        model = Person
        fields = ("username","first_name","last_name","phone_number","email")
        
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

