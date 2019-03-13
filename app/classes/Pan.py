from app.Classes import Pallet, Delivery
from copy import deepcopy
from random import randint
from app.models import PanCoordinator as Coord
from app import db
# from math import ceil


class Pan(object):

    """ A pan object for the sealanes prototype: have the following attributes:

    Attributes:
        pan_id: an unique int identifier to identify a pan with.
        pallets: the pallets of list identifier to identify a pan with.
    """

    # Constructor
    def __init__(self, pan_id: int, pan_width: float, pan_length: float, pan_height: float, pan_rail_height: float,
                 delivery: Delivery, pallets: Pallet):
        """ Return a Pan object."""
        self._pan_id = pan_id
        self._width = pan_width
        self._length = pan_length
        self._height = pan_height
        self._delivery = delivery
        self._pallets = deepcopy(pallets)
        self._freezer_list = []
        self._dry_list = []
        self._cool_list = []
        self._pan_rail_height = pan_rail_height

    # Retrieves a pallet information
    def get_pallet_information(self, pallet_id: int):
        # Iterates through the pallet list and returns the pallet information
        # if found otherwise returns an empty dictionary
        for pi in self._pallets:
            if self._pallets[pi].keys() == pallet_id:
                return self._pallets[pi][pallet_id]
            else:
                return {}

    def add_pallet(self, pallet: Pallet):
        if pallet.category is 'f' or pallet.category is 'F':
            try:
                self._freezer_list.index(pallet)
            except ValueError:
                self._freezer_list.append(deepcopy(pallet))
        elif pallet.category is 'c' or pallet.category is 'C':
            try:
                self._cool_list.index(pallet)
            except ValueError:
                self._cool_list.append(deepcopy(pallet))
        elif pallet.category is 'd' or pallet.category is 'D':
            try:
                self._dry_list.index(pallet)
            except ValueError:
                self._dry_list.append(deepcopy(pallet))
        else:
            return -1

        return 0

    def get_freeze_pos(self):
        return self.matching(self.weight_distribution(self.first_fit_decreasing(self._freezer_list), reverse=True))

    def get_cool_pos(self):
        return self.matching(self.weight_distribution(self.first_fit_decreasing(self._cool_list), reverse=True))

    def get_dry_pos(self):
        return self.matching(self.weight_distribution(self.first_fit_decreasing(self._dry_list), reverse=True))

    def get_full_container(self):
        return self._length_weight_check(self.get_freeze_pos() + self.get_cool_pos() + self.get_dry_pos())

    def get_wasted_space(self, container):
        wasted_space = []

        for bins in container:
            try:
                rail = bins.index("rail")
                space_used = 0
                inner_space = []
                for num in range(0, rail):
                    space_used += bins[num].height

                inner_space.append(1.2 - space_used)
                space_used = 0
                for num_2 in range(rail+1, len(bins)):
                    space_used += bins[num_2].height

                inner_space.append(1.2 - space_used)

                wasted_space.append(inner_space)
            except ValueError:
                space_used = 0
                for pals in bins:
                    space_used += pals.height

                wasted_space.append(self._height - space_used)

        return wasted_space

    def distribution(self, pallets: Pallet):

        # This method assigns the pallets to the correct "bins"

        # This are just trial methods actual stuff will require information gathering

        # available_space_after_rail = 6

        height = 0

        # We need to find the lower bound of for the items height.
        # The list should be sorted using height first.
        # Otherwise the algorithm resembles a first fit algorithm
        # instead of the intended first fit decreasing algorithm
        for pallet in pallets:
            height += pallet.height

        # lower_bound = int(ceil(height / self._height))

        container = [[]]

        for pallet in pallets:
            if len(container) == 0:
                container[0].append(pallet)
                pallet.into_bin = True
            else:
                for bins in container:
                    if len(bins) == 0 and pallet.into_bin is False and pallet.height < self._height:
                        bins.append(pallet)
                        break
                    else:
                        height = 0
                        for pal in bins:
                            if pal == "*":
                                height += 1 + (6 - bins[0].height)
                            else:
                                height += pal.height

                        if height < 6 and pallet.height < 6:
                            bins.append("*")
                            bins.append(pallet)
                            pallet.into_bin = True
                            break
                        elif height + pallet.height < self._height:
                            bins.append(pallet)
                            pallet.into_bin = True
                            break
                        else:
                            ci = container.index(bins)

                            try:
                                container[ci+1]
                            except IndexError:
                                container.append([])

        # Checking whether a pallet is stack_able and swap if it is
        for bins in container:
            for pal2 in range(len(bins)-1,0,-1):
                for li in range(pal2):
                    if bins[li+1] == "*":
                        if bins[li].weight < bins[li + 2].weight:
                            temp_pallet = bins[li]
                            bins[li] = bins[li + 2]
                            bins[li + 2] = temp_pallet
                            del temp_pallet
                        if len(bins) is 4:
                            if bins[li].weight < bins[li + 3].weight:
                                temp_pallet = bins[li]
                                bins[li] = bins[li + 3]
                                bins[li + 3] = temp_pallet
                                del temp_pallet
                    elif bins[li] == "*":
                        continue
                    elif bins[li].weight < bins[li + 1].weight:
                        temp_pallet = bins[li]
                        bins[li] = bins[li + 1]
                        bins[li + 1] = temp_pallet
                        del temp_pallet

        return container

    # Still has internal sacking probelm and stll stacks false on false

    def distribution_2(self, pallets: Pallet):

        container = []
        flag = False

        # Something about vegetables and it not being close to freezer wall
        for pallet in pallets:
            if len(container) == 0:
                container.append([])
                pallet.into_bin = True
                container[0].append(pallet)
            else:
                for bins in container:
                    if len(bins) == 0:
                        pallet.into_bin = True
                        bins.append(pallet)
                        # print("new bin")
                        break
                    else:
                        try:
                            bi = bins.index("rail")
                            height = 0

                            for il in range(0, bi):
                                height += bins[il].height

                            if height + pallet.height < 1.2:
                                if bins[bi - 1].stack_able is True and bins[bi - 1].weight > pallet.weight:
                                    pallet.into_bin = True
                                    bins.insert(bi, pallet)
                                    break
                                elif bins[bi - 1].weight < pallet.weight and pallet.stack_able is True:
                                    temp = bins[bi - 1]
                                    pallet.into_bin = True
                                    bins[bi - 1] = deepcopy(pallet)
                                    bins.append(temp)
                                    break
                        except ValueError:
                            pass

                        height = 0
                        for pal in bins:
                            if pal == "rail":
                                height += 0.2 + (1.2 - height)
                            else:
                                height += pal.height

                        # print("height ", height, " Pallet Height ", pallet.height)

                        if height < 1.2 and pallet.height < 1.2:
                            if height + pallet.height < 1.2:
                                # print("bins <6 height ", len(bins))
                                if bins[0].weight < pallet.weight and pallet.stack_able is True:
                                    temp = bins[0]
                                    pallet.into_bin = True
                                    bins[0] = deepcopy(pallet)
                                    bins.append(temp)
                                    break
                                elif bins[0].weight > pallet.weight and bins[0].stack_able is True:
                                    pallet.into_bin = True
                                    bins.append(pallet)
                                    break
                                else:
                                    bins.append("rail")
                                    pallet.into_bin = True
                                    bins.append(pallet)
                                    break
                            else:
                                try:
                                    for num in range(bins.index("rail"), len(bins)):
                                        if bins[num].weight > pallet.weight and bins[num].stack_able is True:
                                            pallet.into_bin = True
                                            bins.append(pallet)
                                            flag = True
                                            break
                                        elif bins[num].weight < pallet.weight and pallet.stack_able is True:
                                            temp = bins[num]
                                            pallet.into_bin = True
                                            bins[num] = deepcopy(pallet)
                                            bins.append(temp)
                                            flag = True
                                            break

                                    if flag is True:
                                        flag = False
                                        break

                                except ValueError:
                                    bins.append("rail")
                                    pallet.into_bin = True
                                    bins.append(pallet)
                                    break

                            if pallet.into_bin is False:
                                ci = container.index(bins)

                                try:
                                    container[ci + 1]
                                except IndexError:
                                    # print("Cont new bin created")
                                    pallet.into_bin = True
                                    container.append([pallet])
                                    break
                                    # print("Bins in cont ", len(cont))

                        elif height + pallet.height < self._height:
                            if len(bins) == 1:
                                if bins[0].weight > pallet.weight and bins[0].stack_able is True:
                                    pallet.into_bin = True
                                    bins.append(pallet)
                                    break
                                elif bins[0].weight < pallet.weight and pallet.stack_able is True:
                                    temp = bins[0]
                                    pallet.into_bin = True
                                    bins[0] = deepcopy(pallet)
                                    bins.append(temp)
                                    break
                            elif len(bins) > 1:
                                outer_flag = False

                                try:
                                    ind = bins.index("rail")

                                    height = 0

                                    for il in range(ind+1, len(bins)):
                                        height += bins[il].height

                                    if height + pallet.height < 1.2:
                                        for il in range(ind+1, len(bins)):
                                            if bins[il].weight > pallet.weight and bins[il].stack_able is True:
                                                try:
                                                    for il2 in range(il+1, len(bins)):
                                                        pass
                                                except IndexError:
                                                    pallet.into_bin = True
                                                    bins.append(pallet)
                                                    outer_flag = False
                                                    break

                                        if outer_flag is True:
                                            break
                                except ValueError:
                                    pass
                                for p in range(len(bins)):
                                    inner_flag = False

                                    if bins[p] is "rail":
                                        continue
                                    elif bins[p].weight < pallet.weight \
                                            and pallet.stack_able is True:
                                        pallet.into_bin = True
                                        bins.insert(p, pallet)
                                        outer_flag = True
                                        break
                                    elif bins[p] is not "rail" and bins[p].weight > pallet.weight \
                                            and bins[p].stack_able is True:
                                        for inner_p in range(p, len(bins)):
                                            if bins[inner_p] is not "rail" and bins[inner_p]. weight < pallet.weight \
                                                    and pallet.stack_able is True:
                                                pallet.into_bin = True
                                                bins.insert(inner_p, pallet)
                                                inner_flag = True
                                                break
                                            elif bins[inner_p] is not "rail" and bins[inner_p].weight > pallet.weight \
                                                    and bins[inner_p].stack_able is True:
                                                pallet.into_bin = True
                                                bins.insert(inner_p+1, pallet)
                                                inner_flag = True
                                                break
                                        if inner_flag is True:
                                            outer_flag = True
                                            break
                                if outer_flag is True:
                                    break
                ci = container.index(bins)

                try:
                    container[ci + 1]
                except IndexError:
                    # print("Cont new bin created")
                    container.append([])
                    # print("Bins in cont ", len(cont))

        return container

    # The following function assumes that the height of the pallets lies in the range of
    # 0.5 metres to the height of the pan
    def first_fit_decreasing(self, pallets: Pallet):

        # The function uses an algorithm of the same name.
        # The original algorithm requires the calculation of the lower bound, this is to allow an optimal
        # number of bins to be created. Bins in this context refers to available segment space within a body.
        # For the current situation an optimal number of bins would be 22 or less.
        # However, the function will be used independently for each of the required section, as such an optimal number
        # is not known.

        # Initializes an empty pan/container
        container = []
        # Assuming the height of the rail is 0.2 metres
        rail_height = 0.2
        # Assuming the height to rail and after rail is 1.2 metres
        height_to_rail = 1.2

        for pallet in pallets:
            # For a new Pan, create a new bin then insert the pallet into the Bin and move onto the next pallet
            if len(container) == 0:
                pallet.into_bin = True # Not necessarily required, will think about removing it
                temp = deepcopy(pallet)
                container.append([temp])
                continue

            # Checking through all the bins and comparing the height as well as company constraints
            for bins in container:
                # for every new empty bin, insert a pallet and move onto the next pallet
                if len(bins) == 0:
                    pallet.into_bin = True
                    bins.append(pallet)
                    break
                # Calculating the height of the pallets in the bins
                height = 0.0
                for pal in bins:
                    if pal is "rail":
                        height += rail_height + (height_to_rail - height)
                    else:
                        height += pal.height

                if height < height_to_rail and pallet.height < height_to_rail:
                    if height + pallet.height < height_to_rail:
                        if self._height_check(bins, bins[0], pallet):
                            break
                        else:
                            if pallets.index(pallet) == len(pallets)-1:
                                bins.append("rail")
                                pallet.into_bin = True
                                bins.append(pallet)
                                break # Ask about rail placement in the next meeting
                    else:
                        bins.append("rail")
                        pallet.into_bin = True
                        bins.append(pallet)
                        break
                elif height + pallet.height < self._height:
                    if len(bins) == 1:
                        if self._height_check(bins, bins[0], pallet):
                            break

                ci = container.index(bins)

                try:
                    container[ci + 1]
                except IndexError:
                    # print("Cont new bin created")
                    container.append([])
                    # print("Bins in cont ", len(cont))

        return container

    @staticmethod
    def _height_check(bins, pallet1, pallet2):
        if pallet1.stack_able is True and pallet1.weight > pallet2.weight:
            pallet2.into_bin = True
            bins.append(pallet2)
            return True
        elif pallet2.stack_able is True and pallet2.weight > pallet1.weight:
            pallet2.into_bin = True
            bins.insert(0, pallet2)
            return True

        return False

    # Checking weight along the length of the pan rearrange. Get errors and reduce the errors
    def weight_distribution(self, container, reverse=True):
        l = []
        e = []
        g = []

        if len(container) > 1:
            pivot = container[0]
            w_pivot = self._aggregated_weight(pivot)

            for bins in container:

                weight = self._aggregated_weight(bins)

                if weight < w_pivot:
                    l.append(bins)
                elif weight > w_pivot:
                    g.append(bins)
                else:
                    e.append(bins)

            if reverse is True:
                return self.weight_distribution(g, reverse) + e + self.weight_distribution(l, reverse)
            else:
                return self.weight_distribution(l, reverse) + e + self.weight_distribution(g, reverse)
        else:
            return container

    @staticmethod
    def _aggregated_weight(bins):
        weight = 0

        for pal in bins:
            if pal is "rail":
                weight += 0.5
            else:
                weight += pal.weight

        return weight

    def matching(self, container):

        for num_1 in range(len(container)):
            if num_1 % 2 != 0:
                continue
            for num_2 in range(num_1+1, len(container)):
                if self._contains_rail(container[num_1]) is True and self._contains_rail(container[num_2]) is True:
                    container.insert(num_1+1, container.pop(num_2))
                    break
                elif self._contains_rail(container[num_1]) is False and self._contains_rail(container[num_2]) is False:
                    container.insert(num_1+1, container.pop(num_2))
                    break

        return container

    @staticmethod
    def _contains_rail(bins):
        try:
            bins.index("rail")
            return True
        except ValueError:
            return False

    def _length_weight_check(self, container):

        while True:
            weight_even = 0
            weight_odd = 0
            rnd = randint(0, len(container)-2)
            for num_odd in range(len(container)):
                if num_odd % 2 == 1:
                    weight_odd += self._aggregated_weight(container[num_odd])

            for num_even in range(len(container)):
                if num_even % 2 == 0:
                    weight_even += self._aggregated_weight(container[num_even])

            error = abs(weight_odd - weight_even)

            if error < 0.05:
                break
            else:
                if rnd % 2 == 0:
                    container.insert(rnd, container.pop(rnd+1))
                else:
                    container.insert(rnd-1, container.pop(rnd))

        return container

    def to_pan_coord_table(self):
        cont = self.get_full_container()

        del_t = Coord.__table__.delete().where(Coord.delivery_id == self._delivery.delivery_id)
        db.engine.execute(del_t)
        db.session.commit()

        len_coord = -1

        for length in range(len(cont)):
            if length % 2 == 0:
                len_coord += 1

            if length % 2 != 0:
                wid_coord = 1
            else:
                wid_coord = 0

            above_rail = False
            hgh_coord = 0
            for height in range(len(cont[length])):
                if cont[length][height] == 'rail':
                    above_rail = True
                    continue

                c = Coord(
                    pallet_id=cont[length][height].pallet_id,
                    length_position=len_coord,
                    width_position=wid_coord,
                    height_position=hgh_coord,
                    above_rail=above_rail,
                    delivery_id=self._delivery.delivery_id
                )

                db.session.add(c)
                db.session.commit()

                hgh_coord += 1

"""
if __name__ == "__main__":
    from app.Classes import Pallet, Contents
    import random

    dev = Delivery.Delivery(1, "This street")
    pan = Pan(1, 13.4, 126.0, 2.600, dev, [])

    freeze_range = 16
    cool_range = 14
    dry_range = 14
    h = 0.7
    h1 = 1.3

    for freeze in range(freeze_range):
        num = round(random.uniform(0,1), 3)
        if num > 0.8:
            flag = False
        else:
            flag = True

        pal = Pallet.Pallet(freeze, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'F', flag,
                         Contents.Content(1, "Bleh"))
        pan.add_pallet(pal)

    for cool in range(cool_range):
        if num > 0.8:
            flag = False
        else:
            flag = True

        pal = Pallet.Pallet(cool, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'C', flag,
                         Contents.Content(1, "Bleh"))
        pan.add_pallet(pal)

    for dry in range(dry_range):
        if num > 0.8:
            flag = False
        else:
            flag = True

        pal = Pallet.Pallet(dry, round(random.uniform(1, 3), 3), round(random.uniform(h, h1), 3), 'D', flag,
                         Contents.Content(1, "Bleh"))
        pan.add_pallet(pal)

    cont = pan.get_full_container()
    pan.to_pan_coord_table()
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

    space = pan.get_wasted_space(cont)

    for c in space:
        print(c)
"""

