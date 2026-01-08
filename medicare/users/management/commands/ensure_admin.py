from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create multiple admin users'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        admins = [
            {
                'username': os.environ.get('ADMIN1_USERNAME', 'admin-Meriem-Sh'),
                'email': os.environ.get('ADMIN1_EMAIL', 'meriemuncoding@gmail.com'),
                'password': os.environ.get('ADMIN1_PASSWORD', 'Meriem-2003-12-25'),
            },
            {
                'username': os.environ.get('ADMIN2_USERNAME', 'Meriem-Mh'),
                'email': os.environ.get('ADMIN2_EMAIL', 'mahnalmaria@gmail.com'),
                'password': os.environ.get('ADMIN2_PASSWORD', 'Meriem-2004-02-14'),
            },
        ]
        
        for admin_data in admins:
            username = admin_data['username']
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=admin_data['email'],
                    password=admin_data['password']
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" created!'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Superuser "{username}" already exists'))
