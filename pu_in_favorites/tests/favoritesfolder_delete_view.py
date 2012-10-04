import json
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.views.favoritesFolder import FavoritesFolderDeleteView
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from base import FakeRequest


class FavoritesFolderDeleteViewTest(TestCase):

    def setUp(self):

        super(FavoritesFolderDeleteViewTest, self).setUp()
        
        self.view = FavoritesFolderDeleteView.as_view()

    def test_post(self):

        user = User.objects.create(
            username="bobdobalina"
            )

        folder = FavoritesFolder.objects.create(
            _title="Folder", profile=user.get_profile())
 
        self.assertEquals(FavoritesFolder.objects.all().count(), 1)
        
        request = FakeRequest(post={})

        self.view.request = request

        result = self.view(request, pk=folder.pk)

        data = json.loads(result.content)

        self.assertEquals(data['status'], 0)
        self.assertEquals(FavoritesFolder.objects.all().count(), 0)
