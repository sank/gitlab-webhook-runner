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
        settings['path_to_script'],
        int(settings.get('run_timeout_seconds', 15*60)),
        settings.get('log_filename', 'gitlab_webhook.log'),
    )

    authn_policy = GitlabAuthenticationPolicy(settings['gitlab_token'], callback=groupfinder)
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)

    config.add_route('home', '/')
    config.add_route('onpush', '/gitlab/onpush')
    config.add_route('onmerge', '/gitlab/onmerge')

    config.scan()
    return config.make_wsgi_app()
