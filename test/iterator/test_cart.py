import pytest as pytest

from iterator.cart import Cart
from iterator.entities import BaseProduct


@pytest.fixture(scope='class')
def cart_user():
    cart = Cart(
        BaseProduct(uuid='1', title='book'),
        BaseProduct(uuid='2', title='mouse'),
        BaseProduct(uuid='3', title='clock')
    )
    return cart


@pytest.fixture(scope='module')
def cart_user_info():
    return [{'title': 'book'}, {'title': 'mouse'}, {'title': 'clock'}]


def test__get_cart_info(cart_user, cart_user_info):
    assert [cart.product_info for cart in cart_user] == cart_user_info


def test__get_cart_info__out_range(cart_user):
    with pytest.raises(StopIteration):
        ind = 0
        while ind <= cart_user.get_count_product():
            next(cart_user)
            ind += 1
