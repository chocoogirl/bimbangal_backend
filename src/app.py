import falcon
from walrus import Walrus

from .middleware.context import ContextMiddleware
from .model.manager import RedisManager
from .resources.images import ImagesResource
from .resources.text import TextResource


class BimbangalService(falcon.API):
    def __init__(self, cfg):
        super(BimbangalService, self).__init__(
            middleware=[ContextMiddleware()]
        )

        self.cfg = cfg

        # Build an object for Redis Connections
        # Singleton, Dependency Injection
        rds = RedisManager(self.cfg.redis)
        count_block_words = rds.setup()
        print('Created ' , count_block_words , ' number of block words')

        # Create our resources, Dependency Injection
        unsplash_dict, pexels_dict = self.get_dicts(self.cfg.api)
        images_res = ImagesResource(cfg.db['conn'], rds.connection, unsplash_dict, pexels_dict)
        text_res = TextResource(rds.connection)

        # Build routes
        self.add_route('/search', images_res)
        self.add_route('/auto', text_res)

    def get_dicts(self, cfg):
        return (
                {'source': 'Unsplash', 'baseurl': cfg['unsplash']['base_url'], 'params': cfg['unsplash']['params'],
                 'headers': None,
                 'responsekey': cfg['unsplash']['response']['dict_key']},
                {'source': 'Pexels', 'baseurl': cfg['pexels']['base_url'], 'params': cfg['pexels']['params'],
                 'headers': cfg['pexels']['headers'],
                 'responsekey': cfg['pexels']['response']['dict_key']}
        )

    def start(self):
        """ A hook to when a Gunicorn worker calls run()."""
        pass

    def stop(self, signal):
        """ A hook to when a Gunicorn worker starts shutting down. """
        pass
