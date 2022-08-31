import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_book.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

with open("temp.csv", 'w') as f:
    f.write("Username, user_id, email")
    users = User.objects.all()

    for user in users:
        print(f"\n{user.username}, {user.id}, {user.email}")
        f.write(f"\n{user.username}, {user.id}, {user.email}")