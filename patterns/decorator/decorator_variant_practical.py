from abc import ABC, abstractmethod
from typing import List


class Logger(ABC):

    @abstractmethod
    def log(self, message: str):
        ...

    @abstractmethod
    def get_trace(self):
        ...


class FileLogger(Logger):

    def __init__(self, file: List[str]):
        self.file = file

    def log(self, message: str):
        self.file.append(message)

    def get_trace(self):
        return self.file


class SocketLogger(Logger):

    def __init__(self, socket: List[str]):
        self.socket = socket

    def log(self, message: str):
        self.socket.append(message)

    def get_trace(self):
        return self.socket


class LogFilter(Logger):

    def __init__(self, pattern, logger):
        self.pattern = pattern
        self.logger = logger

    def log(self, message: str):
        if self.pattern in message:
            self.logger.log(message)

    def get_trace(self):
        return self.logger.get_trace()


file: List[str] = []
socket: List[str] = []

log_file = LogFilter('error', FileLogger(file))
log_sock = LogFilter('info', SocketLogger(socket))

log_file.log('error 1')
log_file.log('error 2')
log_file.log('info 1')

log_sock.log('error 1')
log_sock.log('info 1')

print(f'File log messages:{log_file.get_trace()}')
print(f'Socket log messages:{log_sock.get_trace()}')
