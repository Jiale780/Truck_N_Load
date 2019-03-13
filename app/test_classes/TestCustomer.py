import unittest
import random
from ..Classes import Customer, Pallet, Contents


class TestCustomer(unittest.TestCase):

    def setUp(self):
        h = 0.5
        h1 = 1.3

        self.cust = Customer.Customer(1234, 'Jack', 'Sparrow', 'Jack Sparrow', 'Jack.Sparrow@email.com',
                                   '42 Hay Street after Well st', 610467938300,
                                   Pallet.Pallet(1, round(random.uniform(1, 3), 3),
                                                 round(random.uniform(h, h1), 3), 'C', False,
                                                 Contents.Content("Meat", 1)))

    def test_customer_id(self):
        self.assertEqual(self.cust.customer_id, 1234)

    def test_first_name(self):
        self.assertEqual(self.cust.first_name, 'Jack')

    def test_last_name(self):
        self.assertEqual(self.cust.last_name, 'Sparrow')

    def test_full_name(self):
        self.assertEqual(self.cust.full_name, 'Jack Sparrow')

    def test_email(self):
        self.assertNotEquals(self.cust.email, 'Tom.Sparrow@email.com')

    def test_address(self):
        self.assertNotEquals(self.cust.address, '13 Collins Street after Well Road')

    def test_phone_number(self):
        self.assertEqual(self.cust.phone_number, 610467938300)


if __name__ == '__main__':
    unittest.main()