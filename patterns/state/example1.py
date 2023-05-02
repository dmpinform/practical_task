from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum


class DoorState(IntEnum):
    OPEN = 1
    CLOSE = 0
    BLOCK = 2


class Door:

    def __init__(self, state):
        self.state = state

    def open(self):
        self.state.open(context=self)

    def close(self):
        self.state.close(context=self)

    def block(self):
        self.state.block(context=self)


@dataclass
class State(ABC):

    @abstractmethod
    def open(self, context: Door):
        ...

    @abstractmethod
    def close(self, context: Door):
        ...

    @abstractmethod
    def block(self, context: Door):
        ...


@dataclass
class StateDoor(State):
    status: DoorState = DoorState.CLOSE

    def open(self, context: Door):
        context.state.status = DoorState.OPEN

    def close(self, context: Door):
        context.state.status = DoorState.CLOSE

    def block(self, context: Door):
        if context.state.status == DoorState.CLOSE:
            context.state.status = DoorState.BLOCK
        else:
            raise 'Сначала закройте дверь'


door = Door(state=StateDoor())
door.open()

print(door.state.status)
door.close()
print(door.state.status)
door.block()
print(door.state.status)
