import unittest

from pyramid import testing


JSON_TEST_MERGE = \
    {
        "object_kind": "merge_request",
        "user":
            {
                "name": "Administrator",
                "username": "root",
            },
        "project":
            {
                "id": 1,
                "url":"http://example.com/gitlabhq/gitlab-test.git",
                "ssh_url":"git@example.com:gitlabhq/gitlab-test.git"
            },
        "repository":
            {
                "name": "Gitlab Test",
                "url": "http://example.com/gitlabhq/gitlab-test.git",
                "description": "Aut reprehenderit ut est.",
                "homepage": "http://example.com/gitlabhq/gitlab-test"
            },
        "object_attributes":
            {
                "id": 99,
                "target_branch": "master",
                "source_branch": "ms-viewport",
            },
    }
JSON_TEST_PUSH = \
    {
        "object_kind": "push",
        "before": "95790bf891e76fee5e1747ab589903a6a1f80f22",
        "after": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
        "ref": "refs/heads/master",
        "project": {
            "id": 15,
            "name": "Diaspora",
            "description": "",
            "web_url": "http://example.com/mike/diaspora",
            "ssh_url": "git@example.com:mike/diaspora.git",
        },
        "repository": {
            "name": "Diaspora",
            "url": "git@example.com:mike/diaspora.git",
            "description": "",
            "homepage": "http://example.com/mike/diaspora",
            "git_http_url": "http://example.com/mike/diaspora.git",
            "git_ssh_url": "git@example.com:mike/diaspora.git",
            "visibility_level": 0
        },
    }


class TestScriptManager(object):
    """
    Script manager for tests
    """
    @staticmethod
    def start(task_data):
        assert task_data.get('action')
        assert task_data.get('project')
        assert task_data.get('branch')


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home_view(self):
        from gitlab_webhook_runner.views import home_view
        request = testing.DummyRequest()
        info = home_view(request)
        self.assertIn('is ready', info)

    def test_onmerge_view(self):
        from gitlab_webhook_runner.views import onmerge_view
        request = testing.DummyRequest()
        request.method = 'POST'
        request.json = JSON_TEST_MERGE
        request.registry.scripts_manager = TestScriptManager()
        info = onmerge_view(request)
        self.assertIn('success', info)
        self.assertTrue(info['success'])

    def test_onpush_view(self):
        from gitlab_webhook_runner.views import onpush_view
        request = testing.DummyRequest()
        request.method = 'POST'
        request.json = JSON_TEST_PUSH
        request.registry.scripts_manager = TestScriptManager()
        info = onpush_view(request)
        self.assertIn('success', info)
        self.assertTrue(info['success'])


class FunctionalTests(unittest.TestCase):
    gitlab_test_token = 'TEST_TOKEN'

    def setUp(self):
        from gitlab_webhook_runner import main
        app = main(
            {},
            gitlab_token=self.gitlab_test_token,
            path_to_script='pwd'
        )
        from webtest import TestApp
        self.testapp = TestApp(app)

    def get_test_header(self):
        return {'X-Gitlab-Token': self.gitlab_test_token}

    def test_home(self):
        res = self.testapp.get('/', status=200, headers=self.get_test_header())
        self.assertTrue(b'is ready' in res.body)

    def test_event_access(self):
        # Check no access (response 403 is normal)
        self.testapp.post_json('/gitlab/onpush', status=403, params={})

    def test_onpush(self):
        # The application accepts onpush commands without errors
        res = self.testapp.post_json(
            '/gitlab/onpush',
            status=200,
            headers=self.get_test_header(),
            params=JSON_TEST_PUSH
        )
        self.assertEqual(res.content_type, 'application/json')
        self.assertIn('success', res.json)
        self.assertTrue(res.json['success'])

    def test_onmerge(self):
        # The application accepts onpush commands without errors
        res = self.testapp.post_json(
            '/gitlab/onmerge',
            status=200,
            headers=self.get_test_header(),
            params=JSON_TEST_MERGE
        )
        self.assertEqual(res.content_type, 'application/json')
        self.assertIn('success', res.json)
        self.assertTrue(res.json['success'])
