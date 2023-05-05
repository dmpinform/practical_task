from abc import ABC
from dataclasses import dataclass


@dataclass
class Compression(ABC):

    def compress(self, path):
        ...


@dataclass
class CompressionZip(Compression):

    def compress(self, path):
        print('ZIP compression')


@dataclass
class CompressionRar(Compression):

    def compress(self, path):
        print('RAR compression')
