'''Admin command implementation for 'initadmin' command.'''

import random
import string

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


def gen_password(length=8):
    '''Generate a random password.'''

    # we use upper and lower case letters and digits for the password
    letters = string.ascii_letters + string.digits

    return ''.join(random.choices(letters, k=length))


class Command(BaseCommand):
    '''Admin command to create an admin user with random password.

    The admin user is only created if no other users are already in the
    database.

    '''

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            print('No users yet in database. Creating admin user.')

            username = 'admin'
            email = 'admin@localhost'
            password = gen_password(8)

            print('Creating account for %s (%s)' % (username, email))

            admin = User.objects.create_superuser(
                email=email,
                username=username,
                password=password)

            admin.is_active = True
            admin.is_admin = True

            admin.save()

            print("Account crated with password '{0}'.".format(password))
            print("Please change password immediately.")
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
