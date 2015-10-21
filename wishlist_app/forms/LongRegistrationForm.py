from django.contrib.auth.forms import UserCreationForm
from django import forms
from wishlist_app.models import User


class LongRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=75)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",)

    def save(self, commit=True):
        user = super(LongRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
