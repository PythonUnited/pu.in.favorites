import logging
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import DetailView
from django.http import Http404
from django.http import HttpResponse
from pgprofile.models.userprofile import UserProfile


log = logging.getLogger("pu_in_favorites")


class FavoritesView(DetailView):

    """ Favoritesview """

    model = UserProfile
    template_name = "favorites_admin.html"
    allowed_actions = ("add_folder", )

    def get_template_names(self):

        return [self.template_name]

    def get_object(self, queryset=None):

        """ Find user profile from logged in user """

        try:
            self.obj = self.request.user.get_profile()
        except:
            raise Http404

        return self.obj

    def post(self, request, *args, **kwargs):

        """ If the request is a POST, handle the request by finding
        the appropriate action, and return the result as JSON"""

        result = {"status": 0, "message": ""}

        if self.request.POST.has_key("action"):
            action = getattr(self, self.request.POST['action'])

            if callable(action) and action in self.allowed_actions:

                self.get_object()
                
                return action()
            else:
                result['status'] = -2
                result['message'] = "Action %s not allowed" % action
        else:
            result["message"] = "No action provided"
            
        return HttpResponse(
            json.dumps(result),
            mimetype='application/json')                 

    def add_folder(self):

        result = {"status": 0, "message": ""}

        if self.request.POST.get("title", None):
            folder = self.obj.favoritesfolder_set.create(
                _title=self.request.POST['title'])
            result["status"] = 0
            result["message"] = "folder %s created" % folder.title
        else:
            result["status"] = -1
            result["message"] = "title is required"
            
        return result
