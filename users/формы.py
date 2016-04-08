# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import Пользователь


class ФормаСозданияПользователя(UserCreationForm):

    class Meta:
        model = Пользователь
        fields = ("имя",)  # используемые поля


class ФормаИзмененияПользователя(UserChangeForm):

    class Meta:
        model = Пользователь
        fields = '__all__'


class ИзменениеПароляПользователяДляАдминистратора(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    required_css_class = 'required'
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ИзменениеПароляПользователяДляАдминистратора,
              self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        """
        Saves the new password.
        """
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    def _get_changed_data(self):
        data = super(ИзменениеПароляПользователяДляАдминистратора,
                     self).changed_data

        for name in self.fields.keys():
            if name not in data:
                return []
        return ['password']
    changed_data = property(_get_changed_data)
