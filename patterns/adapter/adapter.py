from patterns.adapter.entities import Document, Workbook


class DocumentWorkbookAdapter(Document):

    def __init__(self, workbook: Workbook):
        self.workbook = workbook

    def get_name(self) -> str:
        return self.workbook.get_name()

    def get_count_page(self):
        return self.workbook.get_count_sheets()

    def get_author(self) -> str:
        return self.workbook.get_info().get('autor')
