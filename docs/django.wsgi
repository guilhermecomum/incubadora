import os
import sys

path = '/home/metal/work/pixel/incubadora'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'incubadora.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
