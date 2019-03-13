from app.Classes import Contents
from copy import deepcopy


class Pallet(object):
    """ A pallet object for the sealanes prototype: have the following attributes:

    Attributes:
        id: an unique int identifier to identify a pallet with.
        contents: a Content literal representing the pallet's name
        weight: a int literal representing the weight's name
        height: a float literal representing the height's name
        stackable: a bool literal representing the stackable's address
    """

    # Constructor
    def __init__(self, pallet_id: int, weight: float, height: float, pallet_category, stack_able: bool):
        """ Return a Pallet object."""
        if pallet_id < 0 or weight < 0 or height < 0:
            raise ValueError("Values less than Zero have been detected.")
        self._pallet_id = pallet_id
        self._weight = weight
        self._height = height
        self._stack_able = stack_able

        if pallet_category.lower() == 'chill' or pallet_category[0].lower() == 'c' or pallet_category.lower() == 'dry' \
                or pallet_category[0].lower() == 'd' or pallet_category.lower() == 'freeze' \
                or pallet_category[0].lower() == 'f':
            self._pallet_category = pallet_category
        else:
            raise ValueError("Invalid Categories entered")

        self._contents = []
        self._into_bin = False

    @property
    def pallet_id(self, value: int):
        if value < 0:
            raise ValueError("Values less than Zero have been detected.")
        else:
            self._pallet_id = value

    @pallet_id.getter
    def pallet_id(self):
        return self._pallet_id

    @property
    def stack_able(self):
        return self._stack_able

    @property
    def height(self):
        return self._height

    @property
    def category(self):
        return self._pallet_category

    @property
    def weight(self):
        return self._weight

    @property
    def into_bin(self):
        return self._into_bin

    @into_bin.setter
    def into_bin(self, value: bool):
        self._into_bin = value

    @property
    def contents(self):
        return self._contents

    def add_contents(self, content: Contents):
        self._contents.append(deepcopy(content))

    # Retreives the pallet's information in the dictionary structure
    def retrieve_information(self):
        """ Returning a pallet's information"""
        return {"ID": self._pallet_id,
                "Weight": self._weight,
                "Height": self._height,
                "Category": self._pallet_category,
                "Stackable": self._stack_able,
                "Contents": self._contents}

    # Storing the pallet's information to "Ask zach" database
    def store_information(self):
        pass

