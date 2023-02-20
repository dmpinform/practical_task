from imports.engine import EngineBase


class Engine(EngineBase):
    def __init__(self):
        self._info = 'kafka'

    def get_info(self) -> str:
        return self._info


def get_info():
    return 'kafka'
