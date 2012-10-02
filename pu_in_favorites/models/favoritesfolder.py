import logging
from django.db import models


log = logging.getLogger("pu_in_favorites")


class FavoritesFolder(models.Model):

    _title = models.CharField(max_length=250, blank=True, null=True)
    #profiel = models.ForeignKey('UserProfile')

    class Meta:
        app_label = 'pu_in_favorites'

