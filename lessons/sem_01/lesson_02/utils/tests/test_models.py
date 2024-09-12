from typing import Callable
from uuid import uuid4

import pytest

from utils.models import (
    Customer,
    Item,
    Order,
)


class TestOrder:
    ITEMS: list[Item] = [
        Item(label="1", amount=2, price=25),
        Item(label="2", price=50)
    ]
    CUSTOMER: Customer = Customer(
        customer_id=uuid4(),
        username="user#1",
    )

    def test_initialization(self) -> None:
        price_expected = 100

        order = Order(
            customer=self.CUSTOMER,
            items=self.ITEMS,
        )

        assert order.price == price_expected

    def test_get_discounted_price_fail(self) -> None:
        order = Order(
            customer=self.CUSTOMER,
            items=self.ITEMS,
        )

        with pytest.raises(ValueError):
            _ = order.get_discounted_price(
                apply_discount=lambda _: 120,
            )

    @pytest.mark.parametrize(
        "apply_discount,price_expected",
        [
            (lambda _: 20, 80),
            (lambda _: 100, 0),
        ],
        ids=["discount-lt-price", "discount-eq-price"],
    )
    def test_get_discounted_price_success(
        self,
        apply_discount: Callable[[Order], float],
        price_expected: float
    ) -> None:
        order = Order(
            customer=self.CUSTOMER,
            items=self.ITEMS,
        )

        price_discounted = order.get_discounted_price(apply_discount)

        assert price_discounted == price_expected
