from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()  # resolves to accounts.User via AUTH_USER_MODEL


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        # password1 and password2 come from UserCreationForm itself
        fields = ("email", "full_name", "phone")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        # iexact = case-insensitive match, catches any mixed-case duplicates
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email  # the lowercased value is what gets saved