import os
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

from gitlab_webhook_runner.docker_config.config import create_ssh_key, copy_ssh_key_to_host
from gitlab_webhook_runner.docker_config.exceptions import SSHError
from gitlab_webhook_runner.docker_config.ssh_check import check_ssh_connection


def not_docker_result(request):
    request.response.status = 422


@view_config(route_name='docker_config', renderer='templates/docker_config_form.mak', request_method='GET')
def config_form_view(request):
    if request.registry.settings.get('docker') != 'true':
        return HTTPNotFound()
    else:
        return {
            'hostname': os.environ["GITLABWEBHOOK_HOSTNAME"],
            'username': os.environ["GITLABWEBHOOK_USERNAME"]
        }


@view_config(route_name='docker_config', renderer='templates/docker_config_success.mak', request_method='POST')
def config_view(request):
    if request.registry.settings.get('docker') != 'true':
        return HTTPNotFound()

    hostname = os.environ["GITLABWEBHOOK_HOSTNAME"]
    username = os.environ["GITLABWEBHOOK_USERNAME"]

    # Check ssh connection
    check_ssh_connection(
        hostname,
        username=username,
        password=request.params['password']
    )

    # Generate public key for access to server by key
    create_ssh_key(hostname)

    # Copy public key to server
    copy_ssh_key_to_host(
        hostname,
        username,
        request.params['password']
    )

    return {
        'hostname': hostname,
        'username': username
    }


@view_config(context=SSHError,
             route_name='docker_config',
             renderer='templates/docker_config_error.mak',
             request_method='POST')
def config_error(exc, request):
    request.response.status = 422
    return {'errors': exc.messages}
