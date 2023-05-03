from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class State(ABC):

    @abstractmethod
    def next(self, context):
        ...

    @abstractmethod
    def preview(self, context):
        ...

    @abstractmethod
    def get_name(self):
        ...


@dataclass
class Initial(State):

    def next(self, context):
        context.state = Approve()

    def preview(self, context):
        context.state = Initial()

    def get_name(self):
        return 'initial'


@dataclass
class Approve(State):

    def next(self, context):
        context.state = Close()
        context.is_close = True

    def preview(self, context):
        context.state = Initial()

    def get_name(self):
        return 'approve'


@dataclass
class Close(State):

    def next(self, context):
        context.state = Close()

    def preview(self, context):
        context.state = Approve()

    def get_name(self):
        return 'close'
