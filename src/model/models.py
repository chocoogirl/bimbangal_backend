import datetime
from random import shuffle
from mongoengine import Document, StringField, DictField, DateTimeField


class ImageSearchResponse(Document):

    search_term = StringField(required=True, max_length=200)
    source = StringField(required=True, max_length=10)
    api_response = DictField(required=True)
    search_date_time = DateTimeField(default=datetime.datetime.utcnow)


class SearchTermAutoComplete(object):

    def __init__(self, rds):
        self.rds = rds

    def check_stop_words(self, setname, term):
        block_words = self.rds.Set(setname)
        return block_words.__contains__(term.strip())

    def auto_complete(self, search_term):
        response_list = []
        ac = self.rds.autocomplete()
        for value in ac.search(search_term):
            response_list.append(value)
        shuffle(response_list)
        return {"auto_complete": response_list[:5]}

    def store_autocomplete(self, search_term):
        return self.rds.autocomplete().store(search_term.capitalize())
