"""
Bimbangal Backend

Usage:
    bimbangal [options]

Options:
    -h --help                   Show this screen.
"""
import platform
import aumbry
from docopt import docopt
from mongoengine import connect

from .app import BimbangalService
from .config import AppConfig

def main():
    docopt(__doc__)

    cfg = aumbry.load(
        aumbry.FILE,
        AppConfig,
        {
            'CONFIG_FILE_PATH': './src/config/config.yml'
        }
    )

    # Create an instance of the service and serve it
    api_app = BimbangalService(cfg)

    # Check platform whether to run using waitress or gunicorn
    if platform.system() == 'Windows':
        from waitress import serve
        connect(host=cfg.db['conn'])
        serve(api_app, host=cfg.waitress['host'], port=cfg.waitress['port'])
    else:
        from .gunicorn_worker import GunicornApp
        gunicorn_app = GunicornApp(api_app, cfg.gunicorn)
        gunicorn_app.run()
