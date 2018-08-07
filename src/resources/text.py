import falcon
import json

from src.model.models import SearchTermAutoComplete


class TextResource(object):

    def __init__(self, rds):
        self.redis = rds

    def on_get(self, req, resp):
        input_params = req.params
        if 'ac' in input_params:
            stac = SearchTermAutoComplete(self.redis)
            final_response = stac.auto_complete(input_params['ac'])
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(final_response, ensure_ascii=False)
        return resp
