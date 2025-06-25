"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Auto-migrate on startup for Vercel
try:
    from django.core.management import execute_from_command_line
    print("[+] Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("[+] Migrations completed successfully!")
except Exception as e:
    print(f"[-] Migration error (app may still work): {e}")

application = get_wsgi_application()

# Vercel expects 'app' or 'handler' variable
app = application
