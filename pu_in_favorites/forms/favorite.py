from urllib import unquote_plus
from django import forms
from pu_in_favorites.models.favorite import Favorite


class FavoriteForm(forms.ModelForm):

    """ Form for Favorite model """

    order = forms.IntegerField(label="", required=False)

    class Meta:
        model = Favorite
        fields = ("_title", "folder", "uri", "order")

    def save(self, commit=True):

        if "order" in self.changed_data:
            obj_before_change = Favorite.objects.get(pk=self.instance.pk)
            obj_before_change.move(
                dist=(self.instance.order - obj_before_change.order))

        return super(FavoriteForm, self).save(commit=commit)

    def clean_uri(self):
        
        """ Always store the unquoted version """
        
        return unquote_plus(self.cleaned_data['uri'])
