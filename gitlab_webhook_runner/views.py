import os

from pyramid.view import view_config


class NotConfiguredException(Exception):
    pass


def check_configured(request):
    if request.registry.settings.get('docker') == 'true' and not os.environ.get("GITLABWEBHOOK_HOSTNAME"):
        config_url = request.route_url('docker_config')
        raise NotConfiguredException(f'Gitlab webhook runner need to configure! Goto link {config_url}')


@view_config(context=NotConfiguredException, renderer='string')
def not_configured_view(exc, request):
    request.response.status = 422
    return str(exc)


@view_config(route_name='home', renderer='string', permission='runner')
def home_view(request):
    check_configured(request)

    return 'Gitlab webhook runner is ready'


@view_config(route_name='onpush', renderer='json', permission='runner', request_method='POST')
def onpush_view(request):
    check_configured(request)

    branch = request.json.get('ref', '').split('/')[-1]  # Cut branch name from link like "refs/heads/master"
    task_data = \
        {
            'action': request.json.get('object_kind'),
            'project': request.json.get('project', {}).get('ssh_url'),
            'branch': branch,
        }
    request.registry.scripts_manager.start(task_data)
    return {"success": True}


@view_config(route_name='onmerge', renderer='json', permission='runner', request_method='POST')
def onmerge_view(request):
    check_configured(request)

    task_data = \
        {
            'action': request.json.get('object_kind'),
            'project': request.json.get('project', {}).get('ssh_url'),
            'branch': request.json.get('object_attributes', {}).get('target_branch'),
        }
    request.registry.scripts_manager.start(task_data)
    return {"success": True}

