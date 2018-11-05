# coding: UTF-8
import threading
from queue import Empty
import subprocess
import logging
from time import sleep


class ScriptsWorker(threading.Thread):
    """
    Worker for process tasks from queue
    """
    def __init__(self, queue, logger_name, run_timeout_seconds):
        """
        :param queue: Tasks queue
                  Items in queue is dict. Example: {'command': ['/path/to/script.sh', '--param=1']}
        :param logger_name: log name (in config file)
        """
        self.queue = queue
        self.log = logging.getLogger(logger_name)
        self.run_timeout_seconds = run_timeout_seconds
        super(ScriptsWorker, self).__init__()

    @staticmethod
    def exec_command(cmd, run_timeout_seconds, shell=False):
        proc = subprocess.run(
            cmd,
            timeout=run_timeout_seconds,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            shell=shell
        )
        return proc

    def run(self):
        while True:
            try:
                # Get command from task
                task = self.queue.get()
                self.log.info(f'Received new command {task}')
                cmd = task['command']
                # Run process
                proc = self.exec_command(cmd, self.run_timeout_seconds)
                # Write process log
                self.log.info(proc.stdout.decode())
            except subprocess.TimeoutExpired as e:
                # Write process log
                self.log.info(e.stdout.decode())
                self.log.info('ERROR. Process stopped by timeout')
            except Empty:
                sleep(20)
            except Exception as e:
                self.log.exception('Start script error')
                self.log.info(f"ERROR. {str(e)}")


