"""
WSGI config for blog_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 调整这了,将setting配置文件分开加载
profile = os.environ.get('PROJECT_PROFILE', 'develop')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"blog_django.settings.{profile}")

application = get_wsgi_application()
