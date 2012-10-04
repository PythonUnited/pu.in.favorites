from django.conf.urls.defaults import patterns, url
from views.favorites import FavoritesView
from views.favoritesfolder import FavoritesFolderCreateView, \
     FavoritesFolderDetailView, FavoritesFolderUpdateView
from views.favorite import FavoriteCreateView, FavoriteDetailView, \
     FavoriteUpdateView


urlpatterns = patterns("pu_in_favorites.views",
                       
                       url(r"^favorites/favorites",
                           FavoritesView.as_view(),
                           name="pu_in_favorites_favorites"),

                       url(r"favorites/add/favoritesfolder$",
                           FavoritesFolderCreateView.as_view(),
                           name="pu_in_favorites_add_favoritesfolder_json"),
                       
                       url(r"favorites/edit/favoritesfolder/(?P<pk>[\d]+)/",
                           FavoritesFolderUpdateView.as_view(),
                           name="pu_in_favorites_edit_favoritesfolder_json"),
                       
                       url(r"favorites/favoritesfolder/(?P<pk>[\d]+)/",
                           FavoritesFolderDetailView.as_view(),
                           name="pu_in_favorites_view_favoritesfolder_json"),
                       
                       url(r"favorites/favorite/(?P<pk>[\d]+)/",
                           FavoriteDetailView.as_view(),
                           name="pu_in_favorites_view_favorite_json"),
                       
                       url(r"favorites/add/favorite$",
                           FavoriteCreateView.as_view(),
                           name="pu_in_favorites_add_favorite_json"),

                       url(r"favorites/edit/favorite/(?P<pk>[\d]+)/",
                           FavoriteUpdateView.as_view(),
                           name="pu_in_favorites_edit_favorite_json"),
                       )
