from dataclasses import dataclass

from patterns.state.states import Initial, State


@dataclass
class DocumentContext:
    state: State = Initial()
    is_close: bool = False

    def next(self):
        self.state.next(context=self)

    def preview(self):
        self.state.preview(context=self)

    def get_current_state(self):
        return self.state
