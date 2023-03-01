# Пример фабричного метода с виртуальным(обобщенным конструктором)

from abc import ABC, abstractmethod


class Document(ABC):

    @abstractmethod
    def generate(self) -> str:
        ...

    def render(self):
        doc = self.generate()
        print(doc)


class DocumentPdf(Document):

    def generate(self) -> str:
        return 'DOCUMENT PDF'


class DocumentExcel(Document):

    def generate(self) -> str:
        return 'DOCUMENT EXCEL'


class DocumentWord(Document):

    def generate(self) -> str:
        return 'DOCUMENT WORD'


# Это фабричный метод
def CreatorDocument(type_doc: str) -> Document:
    if type_doc == 'EXCEL':
        return DocumentExcel()
    if type_doc == 'WORD':
        return DocumentWord()
    if type_doc == 'PDF':
        return DocumentPdf()


def client_code(doc_type: str):
    document = CreatorDocument(doc_type)
    document.render()


client_code('EXCEL')
client_code('WORD')
client_code('PDF')
