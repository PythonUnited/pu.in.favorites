from django import forms
from pu_in_favorites.models.favorite import Favorite


class FavoriteForm(forms.ModelForm):

    """ Form for Favorite model """

    def __init__(self, *args, **kwargs):

        super(FavoriteForm, self).__init__(*args, **kwargs)

        self.fields['order'].required = False

    class Meta:
        model = Favorite
