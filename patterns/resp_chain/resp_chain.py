from abc import ABC, abstractmethod


class Handler(ABC):
    """
    Абстрактный класс обработчика определяет метод set_next для построения
    цепочки обработчиков и абстрактный метод handle, который будут реализовывать
    конкретные обработчики.
    """

    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    """
    Базовый класс обработчика реализует связывание обработчиков в цепочку.
    """
    _next_handler: Handler = None

    def set_next(self, handler: Handler):
        self._next_handler = handler
        # Возврат обработчика отсюда позволяет связывать обработчики простым способом
        return handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class MailHandler(AbstractHandler):

    def handle(self, request):
        if request == "Mail":
            return f"MailHandler: Я обработал запрос {request}."
        else:
            return super().handle(request)


class PackageHandler(AbstractHandler):

    def handle(self, request):
        if request == "Package":
            return f"PackageHandler: Я обработал запрос {request}."
        else:
            return super().handle(request)


class ComplaintHandler(AbstractHandler):

    def handle(self, request):
        if request == "Complaint":
            return f"ComplaintHandler: Я обработал запрос {request}."
        else:
            return super().handle(request)


if __name__ == "__main__":
    # Построение цепочки
    mail_handler = MailHandler()
    package_handler = PackageHandler()
    complaint_handler = ComplaintHandler()

    mail_handler.set_next(package_handler).set_next(complaint_handler)

    # Отправка запросов
    def client_code(handler: Handler, request):
        result = handler.handle(request)
        if result:
            print(f"  {result}", end="")
        else:
            print(f"  {request} не был обработан.", end="")

    requests = ["Mail", "Package", "Complaint", "Unknown"]
    for request in requests:
        print(f"\nКлиент: Кто может обработать {request}?")
        client_code(mail_handler, request)
