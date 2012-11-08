from django.contrib import admin
from pu_in_favorites.models import Favorite, FavoritesFolder

class FavoriteInline(admin.TabularInline):
    model = Favorite

class FavoritesFolderAdmin(admin.ModelAdmin):
    list_display = ('_title', 'profile', 'num_favorites',)
    search_fields = ['profile__user__username', 'profile__achternaam', '_title', 'favorite___title', 'favorite__uri']
    inlines = [ FavoriteInline, ]

    def num_favorites(self, obj):
        return ("%d" % (obj.favorite_set.count()))
    num_favorites.short_description = 'Number of favorites in this folder'

admin.site.register(FavoritesFolder, FavoritesFolderAdmin)
