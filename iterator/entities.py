from dataclasses import dataclass


@dataclass
class BaseProduct:
    uuid: str
    title: str

    @property
    def product_info(self):
        return {'title': self.title}
