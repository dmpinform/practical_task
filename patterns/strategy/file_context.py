from dataclasses import dataclass

from patterns.strategy.strategy import Compression


@dataclass
class FileContext:
    strategy: Compression
    path: str

    def compress(self):
        self.strategy.compress(path=self.path)
