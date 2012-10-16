from django.template import Library
from pu_in_favorites.util import object_to_urn
from pu_in_favorites.models.favorite import Favorite
from pu_in_favorites.models.favoritesfolder import FavoritesFolder


register = Library()


@register.inclusion_tag('snippets/favoritesfolder.html')
def favoritesfolder(folder):

    return {'object': folder}


@register.inclusion_tag('snippets/favorite.html')
def favorite(favorite):

    return {'object': favorite}


@register.inclusion_tag('snippets/favorite_action.html', takes_context=True)
def favorite_action(context, obj=None, urn=None, title=None):

    """ Render favorite action """

    urn = urn or object_to_urn(obj)
    user_profile = context['request'].user.get_profile()

    try:
        default_folder = user_profile.favoritesfolder_set.all()[0]
    except:
        default_folder = user_profile.favoritesfolder_set.create(_title="General")

    if not title:
        title = obj.title

    try:
        favorite = Favorite.objects.filter(
            folder__profile=user_profile,
            uri=urn)[0]
        is_favorite = True
        favorite_id = favorite.id
    except:
        is_favorite = False
        favorite_id = None        

    return {'is_favorite': is_favorite, 'favorite_id': favorite_id,
            'folders': user_profile.favoritesfolder_set.all(),
            'default_folder': default_folder,
            'urn': urn, 'title': title}
