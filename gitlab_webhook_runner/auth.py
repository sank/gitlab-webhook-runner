# coding: UTF-8
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.decorator import reify
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import Allow
from zope.interface import implementer


def groupfinder(userid, request):
    """
    Callback for roles

    :param userid: principal
    :param request: pyramid request
    :return: list of groups
    """
    return ['group:runner']


class RootFactory(object):
    """ Default factory """
    __acl__ = [(Allow, 'group:runner', 'runner')]

    def __init__(self, request):
        self.request = request


@implementer(IAuthenticationPolicy)
class GitlabAuthenticationPolicy(CallbackAuthenticationPolicy):
    def __init__(self, auth_token, prefix='auth.', callback=None, debug=False):
        self.auth_token = auth_token
        self.callback = callback
        self.prefix = prefix or ''
        self.userid_key = prefix + 'userid'
        self.debug = debug

    def remember(self, request, userid, **kw):
        """ Store a userid in the session."""
        request.session[self.userid_key] = userid
        return []

    def forget(self, request):
        """ Remove the stored userid from the session."""
        if self.userid_key in request.session:
            del request.session[self.userid_key]
        return []

    def unauthenticated_userid(self, request):
        if request.headers.get('X-Gitlab-Token') == self.auth_token:
            return 'runner'

        return None
