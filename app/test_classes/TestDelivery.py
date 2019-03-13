import unittest
from ..Classes import Delivery


class TestDelivery(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.deli1 = Delivery.Delivery(0000, '21 Samson Street after Mary st')
        self.deli2 = Delivery.Delivery(1320, '04 Hill Street after Middle st')

    def test_delivery_id(self):
        print('test_delivery_id')
        self.assertEqual(self.deli1.delivery_id, 0000)
        self.assertEqual(self.deli2.delivery_id, 1320)

    def test_address(self):
        print('test_address')
        self.assertEqual(self.deli1.address, '21 Samson Street after Mary st')
        self.assertEqual(self.deli2.address, '04 Hill Street after Middle st')

        self.deli1.address = 'Road'
        self.deli2.address = 'Street'

        self.assertNotEqual(self.deli1.address, '21 Samson Street after Mary Road')
        self.assertNotEqual(self.deli2.address, '04 Hill Street after Middle Street')

    def retrieve_information(self):

        dict = self.deli1.retrieve_information()
        dict2 = self.deli2.retrieve_information()

        self.assertEqual(dict.get("Delivery ID"), 0000)
        self.assertEqual(dict.get("Delivery address"), '21 Samson Street after Mary st')

        self.assertEqual(dict2.get("Delivery ID"), 1320)
        self.assertNotEqual(dict2.get("Delivery address"), '21 Samson Street after Mary st')


if __name__ == '__main__':
    unittest.TestCase()
