import json
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.views.favoritesfolder import FavoritesFolderDetailView
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from base import FakeRequest


class FavoritesFolderDetailViewTest(TestCase):

    def setUp(self):

        super(FavoritesFolderDetailViewTest, self).setUp()
        
        self.view = FavoritesFolderDetailView.as_view()

    def test_get(self):

        user = User.objects.create(
            username="bobdobalina"
            )

        folder = FavoritesFolder.objects.create(
            _title="Pipo", profile=user.get_profile())
        
        request = FakeRequest(get={})

        self.view.request = request

        result = self.view(request, pk=folder.pk)

        data = json.loads(result.content)

        self.assertEquals(data['_title'], "Pipo")
