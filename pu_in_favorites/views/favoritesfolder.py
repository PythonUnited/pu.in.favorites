from django.core.urlresolvers import reverse
from base import JSONCreateView, JSONDetailView, JSONUpdateView, \
     JSONDeleteView
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from pu_in_favorites.forms.favoritesfolder import FavoritesFolderForm


class FavoritesFolderCreateView(JSONCreateView):

    model = FavoritesFolder
    form_class = FavoritesFolderForm

    def get_success_url(self):

        return reverse("pu_in_favorites_view_favoritesfolder_json",
                       kwargs={'pk': self.object.id})


class FavoritesFolderUpdateView(JSONUpdateView):

    model = FavoritesFolder
    form_class = FavoritesFolderForm

    def get_success_url(self):

        return reverse("pu_in_favorites_view_favoritesfolder_json",
                       kwargs={'pk': self.object.id})    


class FavoritesFolderDetailView(JSONDetailView):

    model = FavoritesFolder


class FavoritesFolderDeleteView(JSONDeleteView):

    model = FavoritesFolder
