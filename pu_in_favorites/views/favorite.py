import json
from django.core.urlresolvers import reverse
from base import JSONCreateView, JSONDetailView, JSONUpdateView, \
     JSONDeleteView
from pu_in_favorites.models.favorite import Favorite
from pu_in_favorites.forms.favorite import FavoriteForm
from pu_in_favorites.templatetags.pu_in_favorites_tags import favorite_action


class FavoriteCreateView(JSONCreateView):

    model = Favorite
    form_class = FavoriteForm

    def get_context_data(self, **kwargs):    

        context = super(FavoriteCreateView, self).get_context_data(**kwargs)

        context['request'] = self.request
        context.update(favorite_action(context, urn=self.object.uri, title=self.object.title))

        return context

    def get_html_template_name(self):

        return "snippets/favorite_action.html"

class FavoriteUpdateView(JSONUpdateView):

    model = Favorite
    form_class = FavoriteForm

    def get_success_url(self):

        return reverse("pu_in_favorites_view_favorite_json",
                       kwargs={'pk': self.object.id})    


class FavoriteDetailView(JSONDetailView):

    model = Favorite


class FavoriteDeleteView(JSONDeleteView):

    model = Favorite

    def get_context_data(self, **kwargs):    

        context = super(FavoriteDeleteView, self).get_context_data(**kwargs)

        context['request'] = self.request
        context.update(favorite_action(context, urn=self.object.uri, title=self.object.title))

        return context

    def get_html_template_name(self):

        return "snippets/favorite_action.html"
