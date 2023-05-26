from typing import Dict


class Workbook:

    def get_name(self):
        return 'MyDocument'

    def get_count_sheets(self):
        return 10

    def get_info(self) -> Dict[str, str]:
        return {'autor': 'Morty', 'create_at': '2000-01-01'}


class Document:

    def get_name(self):
        return 'MyDocument'

    def get_count_page(self):
        return 20

    def get_author(self):
        return 'Rick'
