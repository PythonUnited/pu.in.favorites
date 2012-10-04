import json
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.views.favorite import FavoriteDetailView
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from pu_in_favorites.models.favorite import Favorite
from base import FakeRequest


class FavoriteDetailViewTest(TestCase):

    def setUp(self):

        super(FavoriteDetailViewTest, self).setUp()
        
        self.view = FavoriteDetailView.as_view()

    def test_get(self):

        user = User.objects.create(
            username="bobdobalina"
            )

        folder = FavoritesFolder.objects.create(
            _title="Folder", profile=user.get_profile())
 
        favorite = Favorite.objects.create(
            _title="Favo", folder=folder, uri="http://www.pythonunited.com")
        
        request = FakeRequest(get={})

        self.view.request = request

        result = self.view(request, pk=favorite.pk)

        data = json.loads(result.content)

        self.assertEquals(data['_title'], "Favo")
