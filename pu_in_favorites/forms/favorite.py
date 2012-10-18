from django import forms
from pu_in_favorites.models.favorite import Favorite


class FavoriteForm(forms.ModelForm):

    """ Form for Favorite model """

    class Meta:
        model = Favorite
        fields = ("_title", "folder", "uri",)
