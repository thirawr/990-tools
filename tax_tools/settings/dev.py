from tax_tools.settings.common import *
from tax_tools.settings.private import *

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS += ('debug_toolbar',)
