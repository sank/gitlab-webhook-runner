Gitlab webhook runner README
==================
Automated work with gitlab web hooks

How it work
---------------
- Configure this service:
    - Specify script path to handle web hooks
    - Set url to this service in gitlab
- Gitlab send web hooks to server
- This service listen commands and run script

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

How to read script log execution
---------------
Script output writes to console.
It can be configured in ini file.

Docker
---------------
Access to the launch scripts from the container is realized via ssh transport.
To do this, you need to configure the container to automate the launch of scripts via ssh.
Your server must support access for ssh keys. 
```
docker pull sank16/gitlab-webhook-runner
```

Configure container
```
docker run -p 8888:6543 -e GITLABWEBHOOK_HOSTNAME="ssh-host-name" -e GITLABWEBHOOK_USERNAME=ssh-user-name -e GITLABWEBHOOK_SCRIPTPATH="/path/to/script/on/server" -e GITLABWEBHOOK_TOKEN="PUT-TOKEN-HERE" -it sank16/gitlab-webhook-runner
```
Specify the host, username and password on host, where the script will run.

Start the docker
```
docker start CONTAINER_ID
```

Webhooks gitlab doc
---------------
https://gitlab.com/help/user/project/integrations/webhooks
