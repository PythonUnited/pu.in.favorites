from django.test.testcases import TestCase
from pu_in_favorites.models.favorite import Favorite
from pu_in_favorites.models.favoritesfolder import FavoritesFolder


class FavoriteTest(TestCase):

    def setUp(self):

        super(FavoriteTest, self).setUp()

        self.folder = FavoritesFolder.objects.create(_title="My favorites")

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

        favs = list(self.folder.favorite_set.all().order_by("order"))

        self.assertEquals(favs[0].order, 0)
        self.assertEquals(favs[0].title, "Favorite 0")        
        self.assertEquals(favs[1].order, 1)
        self.assertEquals(favs[1].title, "Favorite 1")                
        self.assertEquals(favs[2].order, 2)
        self.assertEquals(favs[2].title, "Favorite 2")        

        # reorder!
        self.favorite1.move_up()
        favs = list(self.folder.favorite_set.all().order_by("order"))      

        self.assertEquals(favs[0].order, 0)
        self.assertEquals(favs[0].title, "Favorite 1")        
        self.assertEquals(favs[1].order, 1)
        self.assertEquals(favs[1].title, "Favorite 0")                
        self.assertEquals(favs[2].order, 2)
        self.assertEquals(favs[2].title, "Favorite 2")                

        # reorder again...
        self.favorite1.move_up()
        favs = list(self.folder.favorite_set.all().order_by("order"))

        self.assertEquals(favs[0].order, 0)
        self.assertEquals(favs[0].title, "Favorite 1")        
        self.assertEquals(favs[1].order, 1)
        self.assertEquals(favs[1].title, "Favorite 0")                
        self.assertEquals(favs[2].order, 2)
        self.assertEquals(favs[2].title, "Favorite 2")                
