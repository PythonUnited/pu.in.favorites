from django import http
from django.utils import simplejson as json
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import BaseCreateView, BaseUpdateView, \
     BaseDeleteView


class JSONResponseMixin(object):

    def render_to_response(self, context):
        
        "Returns a JSON response containing 'context' as payload"

        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):

        "Construct an `HttpResponse` object."

        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):

        "Convert the context dictionary into a JSON object. Override per view"

        raise NotImplementedError


class JSONUpdateView(JSONResponseMixin, BaseUpdateView):

    def get_form_kwargs(self):

        """
        Returns the keyword arguments for instanciating the form.
        """

        kwargs = super(JSONUpdateView, self).get_form_kwargs()

        data = {}

        self.object = self.get_object()

        for field in self.object.__class__._meta.fields:
            data[field.name] = \
                             field.value_from_object(self.object)

        data.update(kwargs['data'])

        kwargs['data'] = data

        return kwargs

    def convert_context_to_json(self, context):

        return json.dumps({'errors': context['form'].errors,
                           'status': context['form'].is_valid() and 0 or -1})


class JSONCreateView(JSONResponseMixin, BaseCreateView):

    def convert_context_to_json(self, context):

        return json.dumps({'errors': context['form'].errors,
                           'status': context['form'].is_valid() and 0 or -1})


class JSONDetailView(JSONResponseMixin, BaseDetailView):

    def convert_context_to_json(self, context):

        data = {}
        
        for field in self.object.__class__._meta.fields:
            data[field.name] = \
                   field.value_from_object(self.object)

        return json.dumps(data)


class JSONDeleteView(JSONResponseMixin, BaseDeleteView):

    def convert_context_to_json(self, context):

        return "{}"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.delete()

        return http.HttpResponse(
            json.dumps({"status": 0,
                        "message": "deleted object %s" % self.object.id}),
            content_type='application/json')
