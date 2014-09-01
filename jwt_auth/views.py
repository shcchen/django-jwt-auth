from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.core.serializers.json import DjangoJSONEncoder

from jwt_auth.compat import json
from jwt_auth.forms import JSONWebTokenForm


class ObtainJSONWebToken(View):
    http_method_names = ['post']
    error_response_dict = {'errors': ['Improperly formatted request']}
    json_encoder_class = DjangoJSONEncoder

    def post(self, request, *args, **kwargs):
        try:
            request_json = json.loads(request.body)
        except ValueError:
            return self.render_bad_request_response()

        form = JSONWebTokenForm(request_json)

        if not form.is_valid():
            return self.render_bad_request_response({'errors': form.errors})

        context_dict = {
            'token': form.object['token']
        }

        return self.render_response(context_dict)

    def render_response(self, context_dict):
        json_context = json.dumps(context_dict, cls=self.json_encoder_class)

        return HttpResponse(json_context, content_type='application/json')

    def render_bad_request_response(self, error_dict=None):
        if error_dict is None:
            error_dict = self.error_response_dict

        json_context = json.dumps(error_dict, cls=self.json_encoder_class)

        return HttpResponseBadRequest(
            json_context, content_type='application/json')
