# coding: UTF-8
from queue import Queue
from gitlab_webhook_runner.runner.worker import ScriptsWorker


class ScriptsManager(object):
    """
    Script worker manager
    """
    def __init__(self, path_to_script, run_timeout_seconds, logger_name):
        """
        :param path_to_script: Path to script (start on gitlab events)
        :param run_timeout_seconds: Timeout for break script execution
        :param logger_name: log name (in config file)
        """
        self.queue = Queue(maxsize=20)
        self.path_to_script = path_to_script
        self.worker = ScriptsWorker(self.queue, logger_name, run_timeout_seconds)
        self.worker.daemon = True
        self.worker.start()

    def start(self, task_data):
        """
        Run thread if queue is empty
        Otherwise add task to queue

        :param task_data: Parameters for script.
                          {
                              'action': push|merge
                              'project': 'git@example.com:gitlabhq/gitlab-test.git'
                              'branch': branch name, 'master' for example
                          }
        :type task_data: dict
        """
        arguments_map = \
            {
                'action': 'a',
                'project': 'p',
                'branch': 'b',
            }
        task = \
            {
                'command': self.path_to_script +
                           [f'-{arguments_map[k]} {task_data[k]}' for k in task_data if task_data[k]]
            }
        self.queue.put(task)
