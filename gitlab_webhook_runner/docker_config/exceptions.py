# coding: UTF-8


class SSHError(Exception):
    def __init__(self, messages):
        super(Exception, self).__init__(messages[0])
        self.messages = messages
