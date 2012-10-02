from django.conf.urls.defaults import patterns, url
from views.favorites import FavoritesView


urlpatterns = patterns("pu_in_favorites.views",
                       
                       url(r"^favorites/favorites",
                           FavoritesView.as_view(),
                           name="pu_in_favorites_favorites"),

                       url(r"favorites/add_folder",
                           FavoritesView.as_view(),
                           name="pu_in_favorites_add_folder"),
                       
                       )
