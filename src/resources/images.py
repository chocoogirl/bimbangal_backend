import falcon
import json
from mongoengine.queryset.visitor import Q
from mongoengine import connect, connection

from src.model.models import SearchTermAutoComplete, ImageSearchResponse
from src.helpers.generic import GenericHelper


class ImagesResource(object):
    def __init__(self, db, rds, unsplash_dict, pexels_dict):
        self.db = db
        self.redis = rds
        self.unsplash_dict = unsplash_dict
        self.pexels_dict = pexels_dict
        self.db_connection = None

    def connect_to_db(self):
        connection._dbs = {}
        connection._connections = {}
        connection._connection_settings = {}
        self.db_connection = connect(host=self.db)

    def disconnect(self):
        self.db_connection.close()

    def on_get(self, req, resp):
        input_params = req.params
        gh = GenericHelper(self.unsplash_dict, self.pexels_dict)

        self.connect_to_db()

        if 'term' in input_params:
            search_term = input_params['term']
            search_ac = SearchTermAutoComplete(self.redis)

            # If the search term contains stop words send empty response with 404
            if search_ac.check_stop_words('block_words', input_params['term']):
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(dict(searchterm=search_term.capitalize(), photos=''), ensure_ascii=False)
                return resp

            # Check if the search already present if so send existing data
            search_existing_data = []
            for source in ['unsplash', 'pexels']:
                search_term_existing = ImageSearchResponse.objects(Q(source__iexact=source) &
                                                                   Q(search_term__iexact=search_term)) \
                    .only('api_response')
                if search_term_existing:
                    for value in search_term_existing:
                        framed_data = gh.frame_data_response(value.api_response['photos'], source)
                        search_existing_data = framed_data + search_existing_data
            if search_existing_data:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(dict(searchterm=search_term.capitalize(), photos=search_existing_data), ensure_ascii=False)
                self.disconnect()
                return resp

            # Search term passed stop words check and data does not exist
            # Dependency Injection
            searched_data = gh.searchSources(search_term.lower(), search_ac)
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(searched_data, ensure_ascii=False)
            self.disconnect()
            return resp

        if 'pictureid' in input_params:
            search_picture = ImageSearchResponse.objects(Q(api_response__photos__id__iexact=input_params['pictureid']))
            if (search_picture):
                # Search for Picture
                for value in search_picture:
                    stored_api_response = dict(value.api_response)
                    source = value.source
                    search_term = value.search_term
                for index in stored_api_response['photos']:
                    if (str(index['id']) == str(input_params['pictureid'])):
                        response = index
                # Picture found, so frame response
                if (response is not None) and (source is not None):
                    framed_response = gh.frame_data_response([response], source)
                    resp.status = falcon.HTTP_200
                    resp.body = json.dumps(
                        dict(searchterm=search_term.capitalize(), photos=framed_response),
                        ensure_ascii=False)
                    self.disconnect()
                    return resp

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(dict(searchterm=search_term.capitalize(), photos=''), ensure_ascii=False)
        self.disconnect()
        return resp
