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

    def get_template_names(self):

        return [self.template_name]

    def get_object(self, queryset=None):

        self.obj = None

        if not self.kwargs.get("slug", None):
            self.kwargs["slug"] = self.request.user.get_profile().slug

        try:
            self.obj = UserProfile.objects.get(name__iexact=self.kwargs['slug'])
        except ObjectDoesNotExist:
            try:
                self.obj = UserProfile.objects.get(
                    pk=self.kwargs['slug'].split("_")[-1])
            except:
                raise Http404
        except:
            raise Http404

        return self.obj

    def post(self, request, *args, **kwargs):

        if self.request.POST.has_key("action"):
            action = getattr(self, self.request.POST['action'])

            if callable(action):

                self.get_object()
                
                return action()
        else:
            return HttpResponse(
                json.dumps({"status": -2, "message": "no action provided"}),
                mimetype='application/json')                 

    def add_folder(self):

        result = {"status": -1, "message": ""}

        if self.request.POST.get("title", None):
            folder = self.obj.favoritesfolder_set.create(
                _title=self.request.POST['title'])
            result["status"] = 0
            result["message"] = "folder %s created" % folder.title
            
        return HttpResponse(
            json.dumps(result),
            mimetype='application/json')     
