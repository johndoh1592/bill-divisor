from django.db import models
from django.utils.translation import ugettext as _

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User')
