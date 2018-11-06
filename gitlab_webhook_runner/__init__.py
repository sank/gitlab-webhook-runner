import os

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from gitlab_webhook_runner.auth import GitlabAuthenticationPolicy, groupfinder
from gitlab_webhook_runner.runner.manager import ScriptsManager


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(
        settings=settings,
        root_factory='gitlab_webhook_runner.auth.RootFactory',
    )

    config.registry.scripts_manager = ScriptsManager(
        settings['path_to_script'].strip('"').split('" "'),
        int(settings.get('run_timeout_seconds', 15*60)),
        settings.get('runner_logger', 'runner'),
    )

    authn_policy = GitlabAuthenticationPolicy(
        os.environ.get('GITLABWEBHOOK_TOKEN') or settings['gitlab_token'],
        callback=groupfinder
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_mako')

    config.add_route('home', '/')
    config.add_route('docker_config', '/gitlab/docker_config')

    config.add_route('onpush', '/gitlab/onpush')
    config.add_route('onmerge', '/gitlab/onmerge')

    config.scan()
    return config.make_wsgi_app()
