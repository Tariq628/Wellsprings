from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websprings.settings")
django.setup()


def custom_permissions():
    content_type = ContentType.objects.get(app_label="admin_panel", model="Manager")

    # Create specific permissions for Super Admin
    super_admin_group = Group.objects.get(name="SP")
    permission_sp1 = Permission.objects.create(
        codename="super_admin_can_view",
        name="super_admin_can_view_managers",
        content_type=content_type,
    )
    permission_sp2 = Permission.objects.create(
        codename="super_admin_can_delete",
        name="super_admin_can_delete_managers",
        content_type=content_type,
    )
    super_admin_group.permissions.add(permission_sp1, permission_sp2)

    # Create specific permissions for Branch Manager
    permission_bm1 = Permission.objects.create(
        codename="can_create_case_manager",
        name="can_create_case_manager",
        content_type=content_type,
    )
    permission_bm2 = Permission.objects.create(
        codename="can_view_case_manager",
        name="can_view_case_manager",
        content_type=content_type,
    )
    permission_bm3 = Permission.objects.create(
        codename="can_delete_case_manager",
        name="can_delete_case_manager",
        content_type=content_type,
    )
    permission_bm4 = Permission.objects.create(
        codename="can_update_case_manager",
        name="can_update_case_manager",
        content_type=content_type,
    )
    branch_manager = Group.objects.get(name="BM")
    branch_manager.permissions.add(
        permission_bm1, permission_bm2, permission_bm3, permission_bm4
    )

    # Create specific permissions for Case Manager
    permission_cm1 = Permission.objects.create(
        codename="can_create_clients",
        name="can_create_clients",
        content_type=content_type,
    )
    permission_cm2 = Permission.objects.create(
        codename="can_view_clients", name="can_view_clients", content_type=content_type
    )
    permission_cm3 = Permission.objects.create(
        codename="can_delete_clients",
        name="can_delete_clients",
        content_type=content_type,
    )
    permission_cm4 = Permission.objects.create(
        codename="can_update_clients",
        name="can_update_clients",
        content_type=content_type,
    )
    branch_manager = Group.objects.get(name="CM")
    branch_manager.permissions.add(
        permission_cm1, permission_cm2, permission_cm3, permission_cm4
    )


if __name__ == "__main__":
    custom_permissions()
