from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.views.favoritesfolder import FavoritesFolderCreateView
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from base import FakeRequest


class FavoritesFolderCreateViewTest(TestCase):

    def setUp(self):

        super(FavoritesFolderCreateViewTest, self).setUp()
        
        self.view = FavoritesFolderCreateView.as_view()

    def test_post(self):

        user = User.objects.create(
            username="bobdobalina"
            )
        
        request = FakeRequest(
            post={"_title": "pipo", "profile": user.get_profile().pk},
            user=user)

        self.view.request = request

        result = self.view(request)

        self.assertEquals(FavoritesFolder.objects.all().count(), 1)

        request = FakeRequest(
            post={},
            user=user)

        self.view.request = request
        result = self.view(request)

        self.assertEquals(FavoritesFolder.objects.all().count(), 1)
