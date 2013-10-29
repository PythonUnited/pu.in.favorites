import logging
from django.db import models
from pu_in_favorites import settings
from django.conf import settings


log = logging.getLogger("pu_in_favorites")


class FavoritesFolder(models.Model):

    _title = models.CharField(max_length=250)
    profile = models.ForeignKey(settings.DJINN_USERPROFILE_MODEL)
    order = models.IntegerField(default=0)
    can_delete = models.BooleanField(default=True)

    class Meta:
        app_label = 'pu_in_favorites'
        ordering = ["order"]

    @property
    def title(self):

        return self._title

    def clone_for_userprofile(self, userprofile):

        """ Make a copy of this FavoritesFolder, including the connected
        Favorites, and assign it to userprofile """

        clonedfolder, created = FavoritesFolder.objects.get_or_create(
            _title=self._title, profile=userprofile, defaults={
                'order': self.order,
                'can_delete': self.can_delete})

        for fav in self.favorite_set.all():
            fav.clone_to_folder(clonedfolder)

    @staticmethod
    def create_defaults_for(userprofile):
        folders = FavoritesFolder.objects.filter(
            profile__user__username = settings.DEFAULT_FAVORITES_USERNAME)
        for folder in folders:
            folder.clone_for_userprofile(userprofile)
        try:
            return userprofile.favoritesfolder_set.all()[0]
        except:
            return []

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

    def delete(self, *args, **kwargs):

        """ Delete me if you can..."""        

        if self.can_delete:
            super(FavoritesFolder, self).delete(*args, **kwargs)

    def move(self, dist=1):

        direction = (dist > 0 and 1 or -1)

        try:
            targets = list(self.profile.favoritesfolder_set.all())
            target_ids  = [t.pk for t in targets]
            curr_pos = target_ids.index(self.pk)

            if (curr_pos + dist) < 0 or (curr_pos + dist) > len(target_ids):
                return

            target_ids.remove(self.pk)
            target_ids.insert(curr_pos + dist, self.pk)

            for target in targets:
                target.order = target_ids.index(target.pk)
                target.save()

        except:
            log.warn("Couldn't move")
