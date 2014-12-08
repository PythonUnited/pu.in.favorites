import json
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.views.favorite import FavoriteDeleteView
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from pu_in_favorites.models.favorite import Favorite
from base import FakeRequest


class FavoriteDeleteViewTest(TestCase):

    def setUp(self):

        super(FavoriteDeleteViewTest, self).setUp()
        
        self.view = FavoriteDeleteView.as_view()

    def test_post(self):

        user = User.objects.create(
            username="bobdobalina"
            )

        folder = FavoritesFolder.objects.create(
            _title="Folder", profile=user.get_profile())
 
        favorite = Favorite.objects.create(
            _title="Favo", folder=folder, uri="http://www.pythonunited.com")

        self.assertEquals(Favorite.objects.all().count(), 1)
        
        request = FakeRequest(post={}, user=user)

        self.view.request = request

        result = self.view(request, pk=favorite.pk)

        data = json.loads(result.content)

        self.assertEquals(data['status'], 0)
        self.assertEquals(Favorite.objects.all().count(), 0)
