from django.conf.urls import patterns, url
from views.favorites import FavoritesView, FavoritesAdminView
from views.favoritesfolder import FavoritesFolderCreateView, \
     FavoritesFolderDetailView, FavoritesFolderUpdateView, \
     FavoritesFolderDeleteView
from views.favorite import FavoriteCreateView, FavoriteDetailView, \
     FavoriteUpdateView, FavoriteDeleteView


urlpatterns = patterns(
    "pu_in_favorites.views",
    
    url(r"^favorites/favorites/",
        FavoritesView.as_view(),
        name="pu_in_favorites_favorites"),

    url(r"^favorites/favoritesadmin/",
        FavoritesAdminView.as_view(),
        name="pu_in_favorites_favorites_admin"),

    url(r"^favorites/add/favoritesfolder$",
        FavoritesFolderCreateView.as_view(),
        name="pu_in_favorites_add_favoritesfolder_json"),
    
    url(r"^favorites/edit/favoritesfolder/(?P<pk>[\d]+)/?",
        FavoritesFolderUpdateView.as_view(),
        name="pu_in_favorites_edit_favoritesfolder_json"),

    url(r"^favorites/delete/favoritesfolder/(?P<pk>[\d]+)/?",
        FavoritesFolderDeleteView.as_view(),
        name="pu_in_favorites_delete_favoritesfolder_json"),
    
    url(r"^favorites/favoritesfolder/(?P<pk>[\d]+)/?",
        FavoritesFolderDetailView.as_view(),
        name="pu_in_favorites_view_favoritesfolder_json"),
    
    url(r"favorites/favorite/(?P<pk>[\d]+)/?",
        FavoriteDetailView.as_view(),
        name="pu_in_favorites_view_favorite_json"),
    
    url(r"favorites/add/favorite$",
        FavoriteCreateView.as_view(),
        name="pu_in_favorites_add_favorite_json"),

    url(r"favorites/edit/favorite/(?P<pk>[\d]+)/?",
        FavoriteUpdateView.as_view(),
        name="pu_in_favorites_edit_favorite_json"),

    url(r"^favorites/delete/favorite/(?P<pk>[\d]+)/?",
        FavoriteDeleteView.as_view(),
        name="pu_in_favorites_delete_favorite_json"),
    
    )
