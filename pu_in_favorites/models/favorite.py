import logging
from django.db import models
from favoritesfolder import FavoritesFolder
from pu_in_favorites.settings import URN_SCHEMA


log = logging.getLogger("pu_in_favorites")


class Favorite(models.Model):

    """ The favorite class can either point to external resources (by
    using an URL in the uri field, or to internal resources, using an
    URN. """

    _title = models.CharField(max_length=250)
    folder = models.ForeignKey(FavoritesFolder)
    order = models.IntegerField(default=0)
    uri = models.CharField(max_length=2000)

    class Meta:
        app_label = 'pu_in_favorites'

    @property
    def title(self):

        return self._title

    def save(self, **kwargs):

        """ Override save so as to be able to se the order field """

        if not self.pk:
            try:
                _max = Favorite.objects.filter(
                    folder=self.folder).aggregate(models.Max('order'))
                self.order = _max['order__max'] + 1
            except:
                pass
        super(Favorite, self).save(**kwargs)

    def move_up(self):

        _self_order = self.order
        try:
            predecessor = self.folder.favorite_set.get(order=self.order - 1)
            self.order = predecessor.order
            predecessor.order = _self_order
            self.save()
            predecessor.save()
        except:
            log.warn("Couldn't find predecessor. Already first in this folder?")
