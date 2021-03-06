from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

from listing import models

GROUPS_PERMISSIONS = {
    'StandardUser': {
        models.Listing: ['add', 'change', 'delete', 'view']
    },
}

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        for group_name in GROUPS_PERMISSIONS:
            group, created = Group.objects.get_or_create(name=group_name)
            for model_cls in GROUPS_PERMISSIONS[group_name]:
                for perm_index, perm_name in \
                        enumerate(GROUPS_PERMISSIONS[group_name][model_cls]):

                    codename = perm_name + "_" + model_cls._meta.model_name

                    try:
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write("Adding " + codename + " to group " + group.__str__())
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")