# coding: UTF-8
import logging

import paramiko

from gitlab_webhook_runner.docker_config.exceptions import SSHError

log = logging.getLogger(__name__)


def check_ssh_connection(hostname, username, password):
    """
    Check ssh connection
    raise SSHError exception if can`t connect

    :param hostname:
    :param username:
    :param password:
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname,
            username=username,
            password=password
        )
        ssh.close()
    except Exception as e:
        error_text = f'Can`t connect to "{username}@{hostname}"'
        log.exception(error_text)
        raise SSHError(
            [
                error_text,
                f'{error_text}: {str(e)}. Check log'
            ]
        )
