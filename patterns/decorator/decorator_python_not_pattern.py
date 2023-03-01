class Document(object):

    def __init__(self, name):
        self._name = name

    def get_text(self):
        print(f'Document {self._name}')


class Footer(object):

    def __init__(self, document):
        self._document = document

    def __getattr__(self, item):
        return getattr(self._document, item)

    def top(self):
        print(f'{self._document._name} c верхним колонтитулом')


doc = Document('Отчет')

doc_footer = Footer(doc)
doc_footer.get_text()
doc_footer.top()
