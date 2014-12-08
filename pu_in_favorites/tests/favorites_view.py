from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.views.favorites import FavoritesView
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from base import FakeRequest


class FavoritesViewTest(TestCase):

    def setUp(self):

        super(FavoritesViewTest, self).setUp()
        
        self.view = FavoritesView()

    def test_add_folder(self):

        user = User.objects.create(
            username="bobdobalina"
            )
        
        self.view.request = FakeRequest(post={"title": "pipo"}, user=user)
        self.view.get_object()

        self.assertEquals(FavoritesFolder.objects.all().count(), 0)

        result = self.view.add_folder()

        self.assertEquals(FavoritesFolder.objects.all().count(), 1)
        self.assertEquals(FavoritesFolder.objects.all()[0].title, "pipo")
        self.assertEquals(result['status'], 0)

        # Fail on empty title
        #
        self.view.request = FakeRequest(post={})
        
        result = self.view.add_folder()

        self.assertEquals(FavoritesFolder.objects.all().count(), 1)
        self.assertEquals(result['status'], -1)

    def test_rm_folder(self):

        user = User.objects.create(
            username="bobdobalina"
            )

        folder = FavoritesFolder(title="pipo", profile=user.get_profile())
        folder.save()
        
        self.view.request = FakeRequest(post={"folder_id": folder.pk + 10},
                                        user=user)
        self.view.get_object()

        self.assertEquals(FavoritesFolder.objects.all().count(), 1)

        result = self.view.rm_folder()

        self.assertEquals(FavoritesFolder.objects.all().count(), 1)
        self.assertEquals(result['status'], -1)

        self.view.request = FakeRequest(post={"folder_id": folder.pk})

        result = self.view.rm_folder()

        self.assertEquals(FavoritesFolder.objects.all().count(), 0)
        self.assertEquals(result['status'], 0)        
