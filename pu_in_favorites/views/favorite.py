from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from pu_in_content.views.jsonbase import JSONCreateView, JSONDetailView, \
    JSONUpdateView, JSONDeleteView
from pu_in_favorites.models.favorite import Favorite
from pu_in_favorites.forms.favorite import FavoriteForm
from pu_in_favorites.templatetags.pu_in_favorites_tags import favorite_action


class FavoriteCreateView(JSONCreateView):

    model = Favorite
    form_class = FavoriteForm
    success_template_name = "snippets/favorite_action.html"

    def get_context_data(self, **kwargs):    

        context = super(FavoriteCreateView, self).get_context_data(**kwargs)

        context['request'] = self.request

        if self.object:
            context.update(favorite_action(context, 
                                           urn=self.object.uri, 
                                           title=self.object.title,
                                           label_prefix=self.request.REQUEST.get("label_prefix", "")
                                           ))

        return context


class FavoriteUpdateView(JSONUpdateView):

    model = Favorite
    form_class = FavoriteForm
    success_template_name = "snippets/favorite.html"

    def get_context_data(self, **kwargs):

        context = super(FavoriteUpdateView, self).get_context_data(**kwargs)

        context['edit_mode'] = True

        return context


class FavoriteDetailView(JSONDetailView):

    model = Favorite


class FavoriteDeleteView(JSONDeleteView):

    model = Favorite
    template_name = "snippets/favorite_action.html"

    def get_context_data(self, **kwargs):    

        context = super(FavoriteDeleteView, self).get_context_data(**kwargs)

        context['request'] = self.request
        context.update(favorite_action(context, urn=self.object.uri, title=self.object.title, label_prefix=self.request.REQUEST.get("label_prefix", "")))

        return context
