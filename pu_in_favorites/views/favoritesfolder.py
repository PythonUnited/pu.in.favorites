from django.core.urlresolvers import reverse
from pu_in_content.views.jsonbase import JSONCreateView, JSONDetailView, \
    JSONUpdateView, JSONDeleteView
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from pu_in_favorites.forms.favoritesfolder import FavoritesFolderForm


class FavoritesFolderCreateView(JSONCreateView):

    model = FavoritesFolder
    form_class = FavoritesFolderForm

    def get_context_data(self, **kwargs):

        context = super(FavoritesFolderCreateView, self).get_context_data(
            **kwargs)

        context['edit_mode'] = True

        return context

    def get_html_template_name(self):

        return "snippets/favoritesfolder.html"


class FavoritesFolderUpdateView(JSONUpdateView):

    model = FavoritesFolder
    form_class = FavoritesFolderForm

    def get_context_data(self, **kwargs):

        context = super(FavoritesFolderUpdateView, self).get_context_data(
            **kwargs)

        context['edit_mode'] = True

        return context

    def get_html_template_name(self):

        return "snippets/favoritesfolder.html"


class FavoritesFolderDetailView(JSONDetailView):

    model = FavoritesFolder


class FavoritesFolderDeleteView(JSONDeleteView):

    model = FavoritesFolder
