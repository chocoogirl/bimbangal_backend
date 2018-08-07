from random import shuffle
import json
import requests
from src.model.models import SearchTermAutoComplete, ImageSearchResponse

class GenericHelper(object):
    def __init__(self, unsplash_dict, pexels_dict):
        self.unsplash_dict = unsplash_dict
        self.pexels_dict = pexels_dict
        self.api_list = []
        self.api_list.append(self.unsplash_dict)
        self.api_list.append(self.pexels_dict)

    def searchSources(self, search_term, search_ac):
        response_list = self.get_data(self.api_list, search_term, search_ac)
        shuffle(response_list)
        response_dict = {'searchterm': search_term.capitalize(), 'photos': response_list}
        return response_dict

    def get_data(self, api_list, search_term, search_ac):
        response_list = []
        for api_content in api_list:
            photo_search_results = self.get_photos(api_content['baseurl'], api_content['params'],
                                                   api_content['headers'],
                                                   search_term)
            if photo_search_results is not None and photo_search_results[api_content['responsekey']] is not None:
                photo_search_results = self.int2str(photo_search_results, search_term)
                # Got results. Store in DB and autocomplete
                ImageSearchResponse(search_term, api_content['source'].lower(), photo_search_results).save()
                search_ac.store_autocomplete(search_term)
                framed_response_body = self.frame_data_response(photo_search_results[api_content['responsekey']],
                                                            api_content['source'])
                response_list = response_list + framed_response_body

        return response_list

    def get_photos(self, base_url, params, headers, search_term):
        if 'tags' in params:
            params['tags'] = search_term
        elif 'query' in params:
            params['query'] = search_term

        if headers is not None:
            response = requests.get(base_url, params=params, headers=headers)
        else:
            response = requests.get(base_url, params=params)


        if response.status_code == 200:
            response_content = json.loads(response.content)
            if 'results' in response_content:
                response_content['photos'] = response_content.pop('results')
            return response_content
        else:
            return None

    def frame_data_response(self, photo_list, source):
        url_dict = {}
        framed_list = []
        source = source.lower()

        for photo_item in photo_list:
            id = photo_item['id']

            if source == 'unsplash':
                url = photo_item['urls']['small']
                owner = photo_item['user']['name']
                descr = photo_item['description']
                raw_url = photo_item['urls']['regular']
            elif source == 'pexels':
                url = photo_item['src']['medium']
                owner = photo_item['photographer']
                raw_url = photo_item['src']['large']
                temp_descr = photo_item['url']
                temp_descr = temp_descr[:-1]
                temp_descr_modified = temp_descr[temp_descr.rfind('/') + 1:]
                descr = (temp_descr_modified[:temp_descr_modified.rfind('-')]).replace('-', ' ')

            url_dict = {"source": source.capitalize(), "id": id, 'owner': owner.capitalize(), "url": url,
                       "rawurl": raw_url, "description": descr.capitalize()}
            framed_list.append(url_dict)

        return framed_list

    def int2str(self, photo_search_results, search_term):
        for index in photo_search_results['photos']:
            index['id'] = str(index['id'])
            if 'description' in index:
                if index['description'] is None:
                    index['description'] = search_term
        return photo_search_results
