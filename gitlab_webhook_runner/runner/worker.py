# coding: UTF-8
import threading
from datetime import datetime
from queue import Empty
from subprocess import Popen
import subprocess
import logging
from time import sleep

log = logging.getLogger(__name__)


class ScriptsWorker(threading.Thread):
    """
    Worker for process tasks from queue
    """
    def __init__(self, queue, logfile_name, run_timeout_seconds):
        """
        :param queue: Tasks queue
                  Items in queue is dict. Example: {'command': ['/path/to/script.sh', '--param=1']}
        :param logfile_name: log file name
        """
        self.queue = queue
        self.logfile_name = logfile_name
        self.run_timeout_seconds = run_timeout_seconds
        super(ScriptsWorker, self).__init__()

    @staticmethod
    def format_message_for_log(message):
        current_date = str.encode(datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'))
        return b'%s: %s' % (current_date, message)

    def write_log_message(self, logfile, message):
        logfile.write(self.format_message_for_log(message))
        logfile.flush()

    def run(self):
        with open(self.logfile_name, 'ab') as logfile:
            while True:
                try:
                    # Get command from task
                    task = self.queue.get()
                    cmd = task['command']
                    # Run process
                    proc = subprocess.run(
                        cmd,
                        timeout=self.run_timeout_seconds,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                    )
                    # Write process log
                    self.write_log_message(logfile, proc.stdout)
                except subprocess.TimeoutExpired as e:
                    # Write process log
                    self.write_log_message(logfile, e.stdout)
                    self.write_log_message(logfile, b'ERROR. Process stopped by timeout\n')
                except Empty:
                    sleep(20)
                except Exception as e:
                    log.exception('Start script error')
                    error_text = f"ERROR. {str(e)}\n"
                    self.write_log_message(logfile, str.encode(error_text))


