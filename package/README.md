## Описание сборки пакета

### Сборка и публикация в pypi
- Добавить файлы `pyproject.toml`, `setup.cfg`, `setup.py`
- Поставить утилиту для сборки 
  - `python3 -m pip install --upgrade build`
- Задать в cfg имя пакета, который будем собирать 
  - `package_dir = = source` 
  - `[options.packages.find] where = source`
- Импорты внутри пакета поменять относительно `source`
- Запустить сборку 
  - `python3 -m build`
- Поставить утилиту для публикации пакетов 
  - `python3 -m pip install --upgrade twine`
- Опубликовать пакет в pypi 
  - `python3 -m twine upload dist/*`
### Установка пакета из pypi и проверка
- Исключить из сборки основного проекта пакет package
  - `[options.packages.find] exclude = package*`
- Добавить пакет stock-market-adapter==0.0.3 в setup.cfg основного проекта
- Создать "чистую виртуальную среду"
- Установить приложение 
  - `pip install -e .[dev]`
- Запустить тесты
  - `python -m pytest . -vv`

*PS: была проблема со сборкой, решилось этим `apt install python3.10-venv`*