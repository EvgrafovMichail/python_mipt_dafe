from dataclasses import dataclass
from typing import Callable
from uuid import UUID


@dataclass
class Item:
    """
    Товар из Интернет-магазина.

    Attrs:
        label: наименования товара.
        price: цена единицы товара.
        amount: количество товаров. Значение по умолчанию - 1.
    """
    label: str
    price: float
    amount: int = 1


@dataclass
class Customer:
    """
    Основная информация о пользователе Интенет-магазина.

    Attrs:
        customer_id: идентификатор пользователя.
        username: имя пользователя.
        loyalty_points: количество баллов лояльности. Значение по умолчанию - 0.
    """
    customer_id: UUID
    username: str
    loyalty_points: int = 0


class Order:
    """
    Заказ из Интернет-магазина.

    Attrs:
        customer: структура Customer с информацией о покупателе.
        items: список купленных товаров.
        price: стоимость заказа.
    """

    customer: Customer
    items: list[Item]
    price: float

    def __init__(
        self,
        customer: Customer,
        items: list[Item],
    ) -> None:
        """
        Инициализирует заказ.

        При инициализации вычисляется общая стоимость заказа.

        Args:
            customer: информация о покупателе.
            items: список купленных товаров.
        """
        self.customer = customer
        self.items = items
        self.price = sum(
            item.price * item.amount for item in self.items
        )

    def get_discounted_price(
        self, apply_discount: Callable[["Order"], float]
    ) -> float:
        """
        Вычисляет стоимость заказа с учетом примененной скидки.

        Args:
            apply_discount: функция для расчета скидки на основании информации о заказе.

        Returns:
            Число с плавающей точкой - стоимость заказа с учетом скидки.

        Raises:
            ValueError, если расчитанная скидка превышает общую стоимость заказа.
        """
        discount = apply_discount(self)

        if self.price < discount:
            raise ValueError(
                f"discount {discount} is grater than total price {self.price}"
            )

        return self.price - discount
