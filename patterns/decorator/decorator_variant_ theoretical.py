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
        print('some functional')
        return f'ConcreteDecoratorA({self.component.operation()})'


def client_code(component: Component):
    print(f'{component.operation()}')


simple = ConcreteComponent()


decorator1 = ConcreteDecoratorA(simple)
client_code(decorator1)
