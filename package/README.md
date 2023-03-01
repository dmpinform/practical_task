# Описание процесса сборки пакета :

# apt install python3.10-venv
# python3 -m pip install --upgrade build

# задал в cfg пакета, который будем собирать
package_dir =
    = source

[options.packages.find]
where = source

# пути импорта внутри пакета поменял относительно source
# python3 -m build
# python3 -m pip install --upgrade twine
# python3 -m twine upload dist/*

# Исключил из сборки основного проекта пакет package (т.к. будет загружен с pypi)
[options.packages.find]
exclude =
    package*
# Добавил пакет stock-market-adapter==0.0.3 в setup.cfg основного проекта
# pip install -e .[dev]