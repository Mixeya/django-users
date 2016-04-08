# coding=utf-8
from django.db import models
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    AbstractUser, PermissionsMixin, User)
from django.utils import timezone


class МенеджерПользователя(BaseUserManager):
    """
    Имена параметров метода, должны совпадать с реальными
    именами полей, иначе, например, не будет работать команда
    'manage.py createsuperuser
    """
    use_in_migrations = True

    def _create_user(self, имя, почта, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not имя:
            raise ValueError('The given username must be set')
        почта = self.normalize_email(почта)
        user = self.model(имя=имя, почта=почта, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, имя, почта=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(имя, почта, password, **extra_fields)

    def create_superuser(self, имя, почта, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(имя, почта, password, **extra_fields)


class АбстрактныйПользователь(AbstractBaseUser, PermissionsMixin):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.

        Username and password are required. Other fields are optional.
        """
    имя = models.CharField(
        _('name'),
        max_length=30,
        unique=True,
        help_text=_(
            'Required. 30 characters or fewer.'
            ' Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    почта = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = МенеджерПользователя()
    USERNAME_FIELD = 'имя'
    REQUIRED_FIELDS = ['почта', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        # """
        # Returns the first_name plus the last_name, with a space in between.
        # """
        # full_name = '%s %s' % (self.first_name, self.last_name)
        # return full_name.strip()
        pass

    def get_short_name(self):
        # "Returns the short name for the user."
        # return self.first_name
        pass

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Пользователь(АбстрактныйПользователь):
    """
    Признаюсь, я попросту поленился править АбстрактногоПользователя.
    ЭТОТ КЛАСС ПРЕДНАЗНАЧЕН ДЛЯ ИСПОЛЬЗОВАНИЯ.
    """
    pass
