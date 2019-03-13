import unittest
from app.Classes import Pan, Pallet, Delivery, Contents
import random
from copy import deepcopy
from random import randint


class TestPan(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.dev = Delivery.Delivery(1, "This street")
        self.pan = Pan.Pan(1, 13.4, 126.0, 2.600, 3.0, self.dev, [])

    def test_get_pallet_information(self, pallet_id=2890):
        self.assertNotEqual(self.pan.get_pallet_information, pallet_id)

    def test_add_pallet(self):
        freeze_range = 16
        cool_range = 14
        dry_range = 14
        h = 0.7
        h1 = 1.3

        for freeze in range(freeze_range):
            num = round(random.uniform(0, 1), 3)
            if num > 0.8:
                flag = False
            else:
                flag = True

            pal = Pallet.Pallet(freeze, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'F', flag,
                                Contents.Content("Bleh", 1))

            self.pan.add_pallet(pal)
            print(pal)

        for cool in range(cool_range):
            if num > 0.8:
                flag = False
            else:
                flag = True

            pal = Pallet.Pallet(cool, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'C', flag,
                             Contents.Content("Bleh", 1))

            self.pan.add_pallet(pal)
            print(pal)

        for dry in range(dry_range):
            if num > 0.8:
                flag = False
            else:
                flag = True

            pal = Pallet.Pallet(dry, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'D', flag,
                             Contents.Content("Bleh", 1))

            self.pan.add_pallet(pal)
            print(pal)

    def test_get_full_container(self):

        freeze_range = 16
        cool_range = 14
        dry_range = 14
        h = 0.7
        h1 = 1.3

        for freeze in range(freeze_range):
            num = round(random.uniform(0, 1), 3)
            if num > 0.8:
                flag = False
            else:
                flag = True

            pal = Pallet.Pallet(freeze, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'F', flag,
                                Contents.Content("Bleh", 1))
            self.pan.add_pallet(pal)

        for cool in range(cool_range):
            if num > 0.8:
                flag = False
            else:
                flag = True

            pal = Pallet.Pallet(cool, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'C', flag,
                                Contents.Content("Bleh", 1))
            self.pan.add_pallet(pal)

        for dry in range(dry_range):
            if num > 0.8:
                flag = False
            else:
                flag = True

            pal = Pallet.Pallet(dry, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'D', flag,
                                Contents.Content("Bleh", 1))
            self.pan.add_pallet(pal)

        cont = self.pan.get_full_container()

        pasp = []
        for b in cont:
            print("[", end=" ")
            for pl in b:
                if pl is "rail":
                    print("rail", end=" ")
                    continue
                else:
                    print(pl.height, end=" ")
                    pasp.append(pl)
            print("]")

        for b in cont:
            print("[", end=" ")
            for pl in b:
                if pl is "rail":
                    print("rail", end=" ")
                    continue
                else:
                    print(pl.category, end=" ")
            print("]")

        print(len(cont))

        print(len(pasp))

    def test_get_wasted_space(self):
        freeze_range = 16
        cool_range = 14
        dry_range = 14
        h = 0.7
        h1 = 1.3

        for freeze in range(freeze_range):
            num = round(random.uniform(0, 1), 3)
            if num > 0.8:
                flag = False
            else:
                flag = True

            pal = Pallet.Pallet(freeze, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'F', flag,
                                Contents.Content("Bleh", 1))
            self.pan.add_pallet(pal)

        for cool in range(cool_range):
            if num > 0.8:
                flag = False
            else:
                flag = True

            pal = Pallet.Pallet(cool, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'C', flag,
                                Contents.Content("Bleh", 1))
            self.pan.add_pallet(pal)

        for dry in range(dry_range):
            if num > 0.8:
                flag = False
            else:
                flag = True

            pal = Pallet.Pallet(dry, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'D', flag,
                                Contents.Content("Bleh", 1))
            self.pan.add_pallet(pal)

        cont = self.pan.get_full_container()

        pasp = []
        for b in cont:
            print("[", end=" ")
            for pl in b:
                if pl is "rail":
                    print("rail", end=" ")
                    continue
                else:
                    print(pl.height, end=" ")
                    pasp.append(pl)
            print("]")

        for b in cont:
            print("[", end=" ")
            for pl in b:
                if pl is "rail":
                    print("rail", end=" ")
                    continue
                else:
                    print(pl.category, end=" ")
            print("]")
        print(len(cont))

        print(len(pasp))

        space = self.pan.get_wasted_space(cont)

        for c in space:
            print(c)


if __name__ == '__main__':
    unittest.TestCase()