from django.contrib import admin
from django.apps import apps

from rest_framework.authtoken.models import Token, TokenProxy

app_models = apps.get_models()

# Loop through the models and register each one
for model in app_models:
    if (model == Token or model == TokenProxy):
        continue
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        continue