import unittest
from ..Classes import Pallet, Contents


class TestPallet(unittest.TestCase):

    def setUp(self):
        self.pall1 = Pallet.Pallet(2890, 4.5, 2.7, 'c', True, Contents.Content("blee", 1))
        self.pall2 = Pallet.Pallet(2700, 6.5, 1.5, 'f', False, Contents.Content("iewo", 2))

    def test_pallet_id(self):
        self.assertEqual(self.pall1.pallet_id, 2890)
        self.assertEqual(self.pall2.pallet_id, 2700)

    def test_weight(self):
        self.assertEqual(self.pall1.weight, 4.5)
        self.assertEqual(self.pall2.weight, 6.5)

    def test_height(self):
        self.assertEqual(self.pall1.height, 2.7)
        self.assertEqual(self.pall2.height, 1.5)

    def test_category(self):
        self.assertEqual(self.pall1.category, 'c')
        self.assertEqual(self.pall2.category, 'f')

    def test_stack_able(self):
        self.assertEqual(self.pall1.stack_able, True)
        self.assertEqual(self.pall2.stack_able, False)


if __name__ == '__main__':
    unittest.main()