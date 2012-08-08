import anuket

from pyramid_beaker import session_factory_from_settings
from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from anuket.models import DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # configure SQLAlchemy
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    config = Configurator(settings=settings)
#    config.add_route('home', '/')

    # configure session
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    # set an auth_user object
    config.set_request_property(anuket.get_auth_user, 'auth_user', reify=True)

    # configure subscribers
    config.include(anuket.subscribers)

    # configure static views
    config.add_static_view('anuket:static', 'anuket:static', cache_max_age=3600)

    # configure routes
    config.include(anuket.views.root)
    config.include(anuket.views.tools)
    config.include(anuket.views.user)

    config.scan('anuket')

    return config.make_wsgi_app()
