from django import forms
from pu_in_favorites.models.favoritesfolder import FavoritesFolder


class FavoritesFolderForm(forms.ModelForm):

    """ Form for FavoritesFolder model """

    #def __init__(self, *args, **kwargs):

    #    super(FavoritesFolderForm, self).__init__(*args, **kwargs)

    #    self.fields['order'].required = False

    class Meta:
        model = FavoritesFolder
        fields = ("_title", "profile",)
