from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.views.favoritesfolder import FavoritesFolderUpdateView
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from base import FakeRequest


class FavoritesFolderUpdateViewTest(TestCase):

    def setUp(self):

        super(FavoritesFolderUpdateViewTest, self).setUp()
        
        self.view = FavoritesFolderUpdateView.as_view()

    def test_post(self):

        user = User.objects.create(
            username="bobdobalina"
            )

        folder = FavoritesFolder.objects.create(_title="Folder0",
                                                profile=user.get_profile())
        
        request = FakeRequest(
            post={"_title": "Pipo"},
            user=user)
        
        self.view.request = request
        
        result = self.view(request, pk=folder.pk)

        self.assertEquals(FavoritesFolder.objects.all().count(), 1)
        self.assertEquals(FavoritesFolder.objects.get(pk=folder.pk).title,
                          "Pipo")

        request = FakeRequest(
            post={"_title": ""},
            user=user)

        self.view.request = request
        result = self.view(request, pk=folder.pk)

        self.assertEquals(FavoritesFolder.objects.all().count(), 1)
        self.assertEquals(FavoritesFolder.objects.get(pk=folder.pk).title,
                          "Pipo")
