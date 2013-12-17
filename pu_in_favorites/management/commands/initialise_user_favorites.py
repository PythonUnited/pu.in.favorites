from optparse import make_option
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pu_in_favorites.models import Favorite, FavoritesFolder
from pu_in_favorites import settings
from djinn_core.utils import object_to_urn
from djinn_profiles.utils import get_userprofile_model


UserProfile = get_userprofile_model()


class Command(BaseCommand):

    help = "Create the default Favorites for all users that do not have Favorites yet"

    option_list = BaseCommand.option_list + (
        make_option('--do-create', '-c',
            action='store_true',
            dest='do-create',
            default=False,
            help='Without this option a dry-run is performed'),
        )


    def handle(self, *args, **options):

        indicator = ''
        if not options['do-create']:
            indicator = 'DRY RUN: '
            print "\nDoing a dry-run\n"

        defaultfavorites_user, created = User.objects.get_or_create(username=settings.DEFAULT_FAVORITES_USERNAME)
        if defaultfavorites_user.get_profile().favoritesfolder_set.count()==0:
            print "#######################################################################################"
            print "# WARNING"
            print "# user %s does not have default favoritesfolders and favorites yet. " % defaultfavorites_user.username
            print "# Add those from the django-admin screens first"
            print "# ...aborted"
            print "#######################################################################################"
            return

        for profile in UserProfile.objects.all():
            if profile.favoritesfolder_set.count()==0:
                print "%sinitialising default favorites for %s" % (indicator, profile.slug)
                if options['do-create']:
                    FavoritesFolder.create_defaults_for(profile)

            if options['do-create']:
                userdefaultfolder = profile.favoritesfolder_set.all()[0]

        if not options['do-create']:
            print "\nend of dry-run\n"
