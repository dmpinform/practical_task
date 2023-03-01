# Пример фабричного метода

from abc import ABC, abstractmethod


class Document(ABC):

    @abstractmethod
    def generate(self) -> str:
        ...


class DocumentPdf(Document):

    def generate(self) -> str:
        return 'DOCUMENT PDF'


class DocumentExcel(Document):

    def generate(self) -> str:
        return 'DOCUMENT EXCEL'


class DocumentWord(Document):

    def generate(self) -> str:
        return 'DOCUMENT WORD'


class CreatorDocument(ABC):

    def render(self):
        doc = self.create_doc().generate()
        print(doc)

    # Это фабричный метод
    @abstractmethod
    def create_doc(self) -> Document:
        ...


class CreatorDocumentPdf(CreatorDocument):

    def create_doc(self) -> Document:
        return DocumentPdf()


class CreatorDocumentExcel(CreatorDocument):

    def create_doc(self) -> Document:
        return DocumentExcel()


class CreatorDocumentWord(CreatorDocument):

    def create_doc(self) -> Document:
        return DocumentWord()


def client_code(creator_document: CreatorDocument):
    creator_document.render()


client_code(CreatorDocumentPdf())
client_code(CreatorDocumentExcel())
client_code(CreatorDocumentWord())
