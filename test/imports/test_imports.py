from imports.rabbit import *
from imports.database import *
from imports.kafka import *


def test__imports_modules__with_same_name_class():
    assert Engine().get_info() == 'kafka'


def test__imports_modules__with_same_name_function():
    assert get_info() == 'kafka'
