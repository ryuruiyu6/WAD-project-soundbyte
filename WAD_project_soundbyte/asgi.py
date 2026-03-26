import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD_project_soundbyte.settings')
application = get_asgi_application()