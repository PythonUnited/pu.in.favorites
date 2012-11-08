from django import forms
from pu_in_favorites.models.favorite import Favorite


class FavoriteForm(forms.ModelForm):

    """ Form for Favorite model """

    move = forms.IntegerField(label="Move to", required=False)

    class Meta:
        model = Favorite
        fields = ("_title", "folder", "uri", "move")

    def save(self, commit=True):

        obj = super(FavoriteForm, self).save(commit=commit)

        move = self.cleaned_data.get('move', 0)

        if move:
            obj.move(dist=move)

        return obj
