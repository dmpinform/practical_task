from patterns.adapter.adapter import DocumentWorkbookAdapter
from patterns.adapter.entities import Document, Workbook


def get_all_documents():
    return [
        DocumentWorkbookAdapter(Workbook()),
        Document(),
    ]
