from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid.security import Authenticated

class Root:
    def __init__(self, request):
        self.__acl__ = [(Allow, Authenticated, 'view')]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(root_factory=Root, settings=settings)

    authn_policy = AuthTktAuthenticationPolicy('secret', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/home')
    config.add_route('login', '/')
    config.add_route('createAccount', '/createAccount')
    config.add_route('openday', '/day')
    config.add_route('logout', '/logout')
    config.add_route('mood', '/mood')
    config.add_route('feeling', '/feeling')
    config.add_route('today', '/today')
    config.add_route('good', '/good')
    config.add_route('bad', '/bad')
    config.add_route('like', '/like')
    config.add_route('hate', '/hate')
    config.add_route('time', '/time')
    config.add_route('moneyPlus', '/moneyPlus')
    config.add_route('moneyMinus', '/moneyMinus')
    config.add_route('quote', '/quote')
    config.add_route('dream', '/dream')
    config.add_route('save', '/save')
    config.scan()
    return config.make_wsgi_app()