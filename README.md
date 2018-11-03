Gitlab webhook runner README
==================
Automated work with gitlab web hooks

Getting Started
---------------

- cd <directory containing this file>
- $VENV/bin/pip install -r requirements.txt
- $VENV/bin/pserve development.ini

How to config integration with gitlab
---------------
- Goto Integrations settings page: <b>Settings / Integrations</b> menu in project on gitlab
- Set secret token in gitlab
- Copy secret token to your ini file (gitlab_token = TOKEN)
- Set url for push events: http://example.com/gitlab/onpush
- Set url for merge events: http://example.com/gitlab/onmerge

Webhooks gitlab doc
---------------
https://gitlab.com/help/user/project/integrations/webhooks