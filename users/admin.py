# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Пользователь
from django.utils.translation import ugettext_lazy as _
from users.формы import ФормаИзмененияПользователя, \
    ФормаСозданияПользователя, ИзменениеПароляПользователяДляАдминистратора


@admin.register(Пользователь)
class ПользовательДляАдминки(UserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('имя', 'password')}),
        (_('Personal info'), {'fields': ('почта', "фамилия")}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('имя', 'password1', 'password2'),
        }),
    )
    form = ФормаИзмененияПользователя
    add_form = ФормаСозданияПользователя
    change_password_form = ИзменениеПароляПользователяДляАдминистратора
    list_display = ('имя', 'почта', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('имя', 'почта')
    ordering = ('имя',)
    filter_horizontal = ('groups', 'user_permissions',)
