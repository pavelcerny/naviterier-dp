import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_demo.settings")
django.setup()

# your code comes here...

from naviterier.views import updateAddressesDbAPI
updateAddressesDbAPI(5)
