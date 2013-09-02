from pu_in_favorites.models import FavoritesFolder
from pgprofile.models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=UserProfile)
def userprofile_post_save(sender, instance, **kwargs):
    if kwargs.get('created', False):
        FavoritesFolder.create_defaults_for(instance)