from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm as UserChangeFormDefault

from users.models import User as MyUser


class UserChangeForm(UserChangeFormDefault):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            "using <a href=\"../password/\">this form</a>.")
    )


class MyUserAdmin(UserAdmin):
    form = UserChangeForm


admin.site.register(MyUser, MyUserAdmin)
