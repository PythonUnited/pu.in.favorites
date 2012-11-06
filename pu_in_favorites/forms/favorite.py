from django import forms
from pu_in_favorites.models.favorite import Favorite


class FavoriteForm(forms.ModelForm):

    """ Form for Favorite model """

    order = forms.IntegerField(label="", required=False)

    class Meta:
        model = Favorite
        fields = ("_title", "folder", "uri", "order")

    def save(self, commit=True):

        reorder = False

        if "order" in self.changed_data:
            reorder = True
            old_order = Favorite.objects.get(pk=self.instance.pk).order

        obj = super(FavoriteForm, self).save(commit=commit)

        if reorder:
            obj.move(dist=(obj.order - old_order))

        return obj
