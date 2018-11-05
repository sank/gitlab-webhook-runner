# coding: UTF-8
import logging
import subprocess
import os

from gitlab_webhook_runner.docker_config.exceptions import SSHError
from gitlab_webhook_runner.runner.worker import ScriptsWorker

log = logging.getLogger('config')


def create_ssh_key(hostname):
    """
    Generate public key for access to server by this key
    raise SSHError exception if can`t create the key file

    :param hostname:
    """
    try:
        keygen_cmd = \
            [
                'ssh-keygen',
                '-f',
                '"/root/.ssh/id_rsa"',
                '-P',
                '""',
                '-C',
                f'"docker@container.{os.environ["HOSTNAME"]}"',
            ]
        proc = ScriptsWorker.exec_command(' '.join(keygen_cmd), 15, shell=True)
        log.info(proc.stdout.decode())
    except subprocess.TimeoutExpired as e:
        # Write process log
        error_text = 'ERROR ssh-keygen. Process stopped by timeout'
        log.error(error_text)
        log.error(e.stdout.decode())
        raise SSHError(
            [
                error_text,
                e.stdout.decode()
            ]
        )
    except Exception as e:
        error_text = 'Generating ssh key error.'
        log.exception(error_text)
        raise SSHError(
            [
                error_text,
                str(e)
            ]
        )


def copy_ssh_key_to_host(hostname, username, password):
    """
    Copy public key to server
    raise SSHError exception if can`t copy the key file

    :param hostname:
    :param username:
    :param password:
    """
    try:
        ssh_copy_cmd = \
            [
                'sshpass',
                '-p',
                password,
                'ssh-copy-id',
                '-i',
                '/root/.ssh/id_rsa',
                '-o',
                'UserKnownHostsFile=/dev/null',
                '-o',
                'StrictHostKeyChecking=no',
                f'{username}@{hostname}',
            ]
        proc = ScriptsWorker.exec_command(' '.join(ssh_copy_cmd), 15, shell=True)
        log.info(proc.stdout.decode())
    except subprocess.TimeoutExpired as e:
        # Write process log
        error_text = 'ERROR ssh_copy_id. Process stopped by timeout'
        log.error(error_text)
        log.error(e.stdout.decode())
        raise SSHError(
            [
                error_text,
                e.stdout.decode()
            ]
        )
    except Exception as e:
        error_text = 'SSH key copy error.'
        log.exception(error_text)
        raise SSHError(
            [
                error_text,
                str(e)
            ]
        )
