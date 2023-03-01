# 1 реализация
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


# 2 реализация
class Component:

    def operation(self) -> str:
        pass


class ConcreteComponent(Component):

    def operation(self) -> str:
        return 'ConcreteComponent'


class Decorator(Component):
    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        return self._component

    def operation(self) -> str:
        return self._component.operation()


class ConcreteDecoratorA(Decorator):

    def operation(self) -> str:
        self.component.operation()
        print('ADD')
        return f'ConcreteDecoratorA({self.component.operation()})'


def client_code(component: Component):
    print(f'{component.operation()}')


simple = ConcreteComponent()


decorator1 = ConcreteDecoratorA(simple)
client_code(decorator1)
