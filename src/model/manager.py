from walrus import Walrus
import json

class RedisManager(object):
    def __init__(self, cfg=None):
        self.blocked_set_name = cfg['setname']
        try:
            self.redis_connection = Walrus(host=cfg['host'], port=cfg['port'], db=cfg['db'])
        except Exception as e:
            print("Exception occured when connecting to Redis :", e)

    @property
    def connection(self):
        return self.redis_connection

    def setup(self):
        # We can setup all DB related pre-operations here.
        # For the sake of simplicity of the app we only try to connect and display errors if any
        try:
            with open('src/model/data/blocked_words.json','r') as f:
                members = json.loads(f.read())
            return self.redis_connection.Set(self.blocked_set_name).add(*members)
        except Exception as e:
            print('Unable to Setup Redis: {}'.format(e))
