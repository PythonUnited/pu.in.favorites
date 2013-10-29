from django.test.testcases import TestCase
from django.contrib.auth.models import User
from pu_in_favorites.models.favoritesfolder import FavoritesFolder
from djinn_profiles.models.userprofile import UserProfile


class FavoritesFolderTest(TestCase):

    def setUp(self):

        super(FavoritesFolderTest, self).setUp()

        User.objects.create(
            username="bobdobalina"
            )

        self.profile = UserProfile.objects.get(name="bobdobalina")

        self.folder0 = FavoritesFolder.objects.create(_title="My favorites",
                                                      profile=self.profile)

        self.folder1 = FavoritesFolder.objects.create(_title="More favorites",
                                                     profile=self.profile)

        self.folder2 = FavoritesFolder.objects.create(_title="Very favorites",
                                                      profile=self.profile) 

    def test_move(self):

        self.assertEquals(self.folder1.order, 1)

        folders = list(self.profile.favoritesfolder_set.all())

        self.assertEquals(folders[0].title, "My favorites")        
        self.assertEquals(folders[1].title, "More favorites")                
        self.assertEquals(folders[2].title, "Very favorites")        

        # reorder!
        self.folder1.move(dist=-1)
        folders = list(self.profile.favoritesfolder_set.all())

        self.assertEquals(folders[0].title, "More favorites") 
        self.assertEquals(folders[1].title, "My favorites")
        self.assertEquals(folders[2].title, "Very favorites")                

        # reorder again...
        self.folder1.move(dist=2)
        folders = list(self.profile.favoritesfolder_set.all())

        self.assertEquals(folders[0].title, "My favorites")        
        self.assertEquals(folders[1].title, "Very favorites")                
        self.assertEquals(folders[2].title, "More favorites")                
