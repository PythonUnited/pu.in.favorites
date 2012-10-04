import json
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.views.favorite import FavoriteCreateView
from pu_in_favorites.models.favorite import Favorite
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from base import FakeRequest


class FavoriteCreateViewTest(TestCase):

    def setUp(self):

        super(FavoriteCreateViewTest, self).setUp()
        
        self.view = FavoriteCreateView.as_view()

    def test_post(self):

        user = User.objects.create(
            username="bobdobalina"
            )

        folder = FavoritesFolder.objects.create(_title="Folder",
                                                profile=user.get_profile())
        
        request = FakeRequest(
            post={"_title": "pipo",
                  "folder": folder.pk,
                  "uri": "http://www.pythonunited.com/"},
            user=user)

        self.view.request = request

        result = self.view(request)

        self.assertEquals(Favorite.objects.all().count(), 1)

        request = FakeRequest(
            post={},
            user=user)

        self.view.request = request
        result = self.view(request)

        self.assertEquals(Favorite.objects.all().count(), 1)

        data = json.loads(result.content)

        self.assertEquals(data['status'], -1)
        
