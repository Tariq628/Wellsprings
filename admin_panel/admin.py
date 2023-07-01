from django.contrib import admin
from .models import Manager


from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        # Check if a new superuser is being created
        if not change and obj.is_superuser:
            group, _ = Group.objects.get_or_create(name="SA")
            obj.groups.add(group)
        super().save_model(request, obj, form, change)


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "user_types", "organisation", "is_verified")

    # Add filter record functionality on te behalf of user_types and is_verified
    list_filter = ("user_types", "is_verified")

    fieldsets = (
        ("Credentials", {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_superuser", "user_permissions", "user_types")},
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    def get_form(self, request, obj=None, **kwargs):
        # Store the request in the form for later use
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "user_types":
            if request.user.user_types == "BM":
                # Limit the choices to only 'BM' (Branch Manager) for superusers and Other Managers
                kwargs["choices"] = [("CM", "Case Manager"), ("client", "Client")]
            if request.user.user_types == "CM":
                # Limit the choices to only 'CM' (Case Manager) for superusers and Other Managers
                kwargs["choices"] = [("client", "Client")]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.user_types == "BM":
            # Filter objects to display only Case Managers
            qs = qs.filter(user_types__in=["CM", "client"])
        elif request.user.user_types == "CM":
            qs = qs.filter(user_types__in=["client"])

        return qs
