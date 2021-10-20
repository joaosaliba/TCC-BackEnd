from django.core.management.base import BaseCommand, CommandError
from rede_auth.models import User
from rede import settings
from datetime import date


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in settings.ADMINS:
            username = user[0].replace(' ', '')
            email = user[1]
            password = 'admin'
            first_name = username.capitalize()

            try:
                admin = User.objects.create_superuser(email=email, username=username, password=password, first_name=first_name, user_type="Admin")
                admin.is_active = True
                admin.is_admin = True
                admin.save()
            except Exception as e:
                print("Usuario {} ja esta criado".format(username))
                print('Erro: {}'.format(e))

