from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.models.favorite import Favorite
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from pgprofile.models.userprofile import UserProfile


class FavoriteTest(TestCase):

    def setUp(self):

        super(FavoriteTest, self).setUp()

        User.objects.create(
            username="bobdobalina"
            )

        profile = UserProfile.objects.get(name="bobdobalina")

        self.folder = FavoritesFolder.objects.create(_title="My favorites",
                                                     profile=profile)

        self.favorite0 = Favorite.objects.create(
            _title="Favorite 0",
            folder=self.folder,
            uri="href://www.pythonunited.com/"
            )
        self.favorite1 = Favorite.objects.create(
            _title="Favorite 1",
            folder=self.folder,
            uri="href://www.pythonunited.com/contact"
            )
        self.favorite2 = Favorite.objects.create(
            _title="Favorite 2",
            folder=self.folder,
            uri="urn:pu.intranet:pu.intranet.news:news:1"
            )

    def test_move_up(self):

        self.assertEquals(self.favorite1.order, 1)

        favs = list(self.folder.favorite_set.all())

        self.assertEquals(favs[0].title, "Favorite 0")        
        self.assertEquals(favs[1].title, "Favorite 1")                
        self.assertEquals(favs[2].title, "Favorite 2")        

        # reorder!
        self.favorite1.move(dist=-1)
        favs = list(self.folder.favorite_set.all())

        self.assertEquals(favs[0].title, "Favorite 1")        
        self.assertEquals(favs[1].title, "Favorite 0")                
        self.assertEquals(favs[2].title, "Favorite 2")                

        # reorder again...
        self.favorite1.move(dist=-1)
        favs = list(self.folder.favorite_set.all())

        self.assertEquals(favs[0].title, "Favorite 1")        
        self.assertEquals(favs[1].title, "Favorite 0")                
        self.assertEquals(favs[2].title, "Favorite 2")                
