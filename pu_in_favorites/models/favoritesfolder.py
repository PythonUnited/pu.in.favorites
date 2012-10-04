import logging
from django.db import models
from pgprofile.models.userprofile import UserProfile


log = logging.getLogger("pu_in_favorites")


class FavoritesFolder(models.Model):

    _title = models.CharField(max_length=250)
    profile = models.ForeignKey(UserProfile)
    order = models.IntegerField(default=0)

    class Meta:
        app_label = 'pu_in_favorites'
        ordering = ["order"]

    @property
    def title(self):

        return self._title

    def save(self, **kwargs):

        """ Override save so as to be able to se the order field """

        if not self.pk:
            try:
                _max = FavoritesFolder.objects.filter(
                    profile=self.profile).aggregate(models.Max('order'))
                self.order = _max['order__max'] + 1
            except:
                self.order = 0
        super(FavoritesFolder, self).save(**kwargs)

    def move(self, dist=1):

        direction = (dist > 0 and 1 or -1)

        try:
            targets = list(self.profile.favoritesfolder_set.filter(
                order__range=(min(self.order + direction, self.order + dist),
                              max(self.order + direction, self.order + dist))))
            self.order = self.order + dist
            self.save()

            for target in targets:
                target.order -= direction
                target.save()
        except:
            log.warn("Couldn't move")
