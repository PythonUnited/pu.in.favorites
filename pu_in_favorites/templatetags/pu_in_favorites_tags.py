from django.template import Library
from pu_in_favorites.util import object_to_urn
from pu_in_favorites.models.favorite import Favorite
from pu_in_favorites.models.favoritesfolder import FavoritesFolder


register = Library()


@register.inclusion_tag('snippets/favoritesfolder.html', takes_context=True)
def favoritesfolder(context, folder, edit_mode="False"):

    edit_mode = (edit_mode and edit_mode != "False")

    return {'object': folder, "edit_mode": edit_mode, 
            'request': context['request']}


@register.inclusion_tag('snippets/favorite.html', takes_context=True)
def favorite(context, favorite, edit_mode="False"):

    edit_mode = (edit_mode and edit_mode != "False")

    if favorite.url.startswith("http") and \
            not favorite.url.startswith(context['request'].get_host()):
        external = True
    else:
        external = False

    return {'object': favorite, "edit_mode": edit_mode, "external": external}


@register.inclusion_tag('snippets/favorite_action.html', takes_context=True)
def favorite_action(context, obj=None, urn=None, title=None, label_prefix="",
                    extra_css_classes=""):

    """ Render favorite action """

    urn = urn or object_to_urn(obj)
    user_profile = context['request'].user.get_profile()
    url = obj.get_absolute_url()

    try:
        default_folder = user_profile.favoritesfolder_set.all()[0]
    except:
        default_folder = FavoritesFolder.create_defaults_for(user_profile)

    if not title:
        title = obj.title

    try:
        favorite = Favorite.objects.filter(
            folder__profile=user_profile,
            uri__in=[urn, url])[0]
        is_favorite = True
        label = "Favoriet"
        favorite_id = favorite.id
    except:
        is_favorite = False
        label = "Favoriet maken"
        favorite_id = None        

    if label_prefix:
        label = "%s %s" % (label_prefix, label.lower())

    return {'is_favorite': is_favorite, 'favorite_id': favorite_id,
            'folders': user_profile.favoritesfolder_set.all(),
            'default_folder': default_folder, 'label': label,
            'extra_css_classes': extra_css_classes,
            'label_prefix': label_prefix,
            'urn': urn, 'title': title,
            'extra_class': extra_class}
