from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

User = get_user_model()  # resolves to accounts.User via AUTH_USER_MODEL


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        # password1 and password2 come from UserCreationForm itself
        fields = ("email", "full_name", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = True

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        # iexact = case-insensitive match, catches any mixed-case duplicates
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email  # the lowercased value is what gets saved


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "phone")

    def __init__(self, *args, **kwargs):          # inside ProfileForm
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = True

def _digits(value):
    # "0801 234-5678" and "08012345678" should count as the same number
    return "".join(c for c in value if c.isdigit())


class PasswordRecoveryForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm new password")

    def clean(self):
        cleaned = super().clean()
        email, phone = cleaned.get("email"), cleaned.get("phone")
        p1, p2 = cleaned.get("new_password1"), cleaned.get("new_password2")

        if p1 and p2 and p1 != p2:
            self.add_error("new_password2", "The two passwords don't match.")
        if p1:
            # strength is checked whether or not the details match, so a weak-password
            # error can never hint that the email and phone were right
            try:
                validate_password(p1)
            except forms.ValidationError as e:
                self.add_error("new_password1", e)

        if email and phone:
            user = User.objects.filter(email__iexact=email.strip(), is_active=True).first()
            digits = _digits(phone)
            # one generic error, so it never says which part was wrong
            if not user or not digits or _digits(user.phone) != digits:
                raise forms.ValidationError("Those details don't match our records.")
            self.user = user  # the view needs this to set the password
        return cleaned

    def save(self):
        self.user.set_password(self.cleaned_data["new_password1"])  # hashes it
        self.user.save(update_fields=["password"])
        return self.user