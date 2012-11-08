import logging
from django.db import models
from django.core.exceptions import ValidationError
from favoritesfolder import FavoritesFolder
from pu_in_favorites.util import urn_to_object


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
        ordering = ["order"]

    @property
    def title(self):

        return self._title

    # make a clone of this Favorite and put it in targetfolder
    def clone_to_folder(self, targetfolder):
        return Favorite.objects.create(_title=self._title, folder=targetfolder, order=self.order, uri=self.uri)

    @property
    def url(self):

        """ If the URI is n URN, resolve to actual object url,
        otherwise leave it """

        if self.uri.startswith("urn:"):
            return urn_to_object(self.uri).get_absolute_url()
        else:
            return self.uri    

    def clean(self):

        if not self.pk:
            try:
                if Favorite.objects.filter(uri=self.uri, 
                                       folder=self.folder).exists():
                    raise ValidationError("Favorite already exists!")
            except:
                pass

    def save(self, **kwargs):

        """ Override save so as to be able to se the order field """

        if not self.pk:
            try:
                _max = Favorite.objects.filter(
                    folder=self.folder).aggregate(models.Max('order'))
                self.order = _max['order__max'] + 1
            except:
                self.order = 0
        super(Favorite, self).save(**kwargs)

    def move(self, dist=1):

        direction = (dist > 0 and 1 or -1)

        try:
            targets = list(self.folder.favorite_set.filter(
                order__range=(min(self.order + direction, self.order + dist),
                              max(self.order + direction, self.order + dist))))
            self.order = self.order + dist
            self.save()

            for target in targets:
                target.order -= direction
                target.save()
        except:
            log.warn("Couldn't move")
