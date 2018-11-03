from subprocess import Popen

from pyramid.view import view_config


@view_config(route_name='home', renderer='string', permission='runner')
def home_view(request):
    return 'Gitlab webhook runner is ready'


@view_config(route_name='onpush', renderer='json', permission='runner', request_method='POST')
def onpush_view(request):
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
    task_data = \
        {
            'action': request.json.get('object_kind'),
            'project': request.json.get('project', {}).get('ssh_url'),
            'branch': request.json.get('object_attributes', {}).get('target_branch'),
        }
    request.registry.scripts_manager.start(task_data)
    return {"success": True}
