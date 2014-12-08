from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.views.favorite import FavoriteUpdateView
from pu_in_favorites.models.favorite import Favorite
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from base import FakeRequest


class FavoriteUpdateViewTest(TestCase):

    def setUp(self):

        super(FavoriteUpdateViewTest, self).setUp()
        
        self.view = FavoriteUpdateView.as_view()

    def test_post(self):

        user = User.objects.create(
            username="bobdobalina"
            )

        folder = FavoritesFolder.objects.create(_title="Folder0",
                                                profile=user.get_profile())

        favorite = Favorite.objects.create(_title="Favorite0",
                                           folder=folder,
                                           uri="http://www.pythonunited.com/"
                                           )
        
        request = FakeRequest(
            post={"_title": "Pipo"},
            user=user)
        
        self.view.request = request
        
        result = self.view(request, pk=folder.pk)

        self.assertEquals(Favorite.objects.all().count(), 1)
        self.assertEquals(Favorite.objects.get(pk=favorite.pk).title,
                          "Pipo")

        request = FakeRequest(
            post={"_title": ""},
            user=user)

        self.view.request = request
        result = self.view(request, pk=favorite.pk)

        self.assertEquals(Favorite.objects.all().count(), 1)
        self.assertEquals(Favorite.objects.get(pk=folder.pk).title,
                          "Pipo")

        # test order
        #
        favorite2 = Favorite.objects.create(_title="Favorite1",
                                            folder=folder,
                                            uri="http://www.pythonunited.com/"
                                            )

        self.assertEquals(Favorite.objects.all()[0].title, "Pipo")

        request = FakeRequest(
            post={"_title": "Pipo", "order": 1},
            user=user)

        self.view.request = request
        result = self.view(request, pk=favorite.pk)

        self.assertEquals(Favorite.objects.all()[1].title, "Pipo")
