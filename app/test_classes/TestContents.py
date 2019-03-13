import unittest
from ..Classes import Contents


class TestContents(unittest.TestCase):

    def setUp(self):
        print('setUp')
        self.cont1 = Contents.Content('BASKET FILTER D.203 X 120', 10)
        self.cont2 = Contents.Content('LEFT COMPACT-JET', 12)

    def tearDown(self):
        print('tearDown\n')

    def test_retrieve_information(self):

        dict = self.cont1.retrieve_contents()
        dict_2 = self.cont2.retrieve_contents()

        self.assertEqual(dict.get("Name"), 'BASKET FILTER D.203 X 120')
        self.assertEqual(dict.get("Quantity"), 10)

        self.assertNotEqual(dict_2.get("Name"), 'BASKET FILTER D.203 X 120')
        self.assertNotEqual(dict_2.get("Quantity"), 10)


if __name__ == '__main__':
    unittest.main()
