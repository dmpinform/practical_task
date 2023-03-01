# Пример фабричного метода с внедренным шаблонным методом

from abc import ABC, abstractmethod


class Document(ABC):

    @abstractmethod
    def generate(self) -> str:
        ...


class DocumentPdf(Document):

    def generate(self) -> str:
        return 'PDF'


class DocumentExcel(Document):

    def generate(self) -> str:
        return 'EXCEL'


class DocumentWord(Document):

    def generate(self) -> str:
        return 'WORD'


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


# Пример c фабричного метода с виртуальным(обобщенным конструктором)
def CreatorDocumentVirtualConstructor(type_doc: str) -> Document:
    if type_doc == 'EXCEL':
        return DocumentExcel()
    if type_doc == 'WORD':
        return DocumentWord()
    if type_doc == 'PDF':
        return DocumentPdf()


def client_code(doc_type: str):
    document = CreatorDocumentVirtualConstructor(doc_type)
    print(document.generate())


client_code('EXCEL')
client_code('WORD')
client_code('PDF')
