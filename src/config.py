from aumbry import Attr, YamlConfig


class AppConfig(YamlConfig):
    __mapping__ = {
        'db': Attr('db', dict),
        'redis': Attr('redis', dict),
        'api': Attr('api', dict),
        'gunicorn': Attr('gunicorn', dict),
        'waitress': Attr('waitress', dict),
    }

    def __init__(self):
        self.gunicorn = {}
