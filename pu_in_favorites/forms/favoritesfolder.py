from django import forms
from pu_in_favorites.models.favoritesfolder import FavoritesFolder


class FavoritesFolderForm(forms.ModelForm):

    """ Form for FavoritesFolder model """

    order = forms.IntegerField(label="", required=False)

    class Meta:
        model = FavoritesFolder
        fields = ("_title", "order", "profile")

    def save(self, commit=True):

        if "order" in self.changed_data:
            obj_before_change = FavoritesFolder.objects.get(pk=self.instance.pk)
            obj_before_change.move(
                dist=(self.instance.order - obj_before_change.order))

        return super(FavoritesFolderForm, self).save(commit=commit)
