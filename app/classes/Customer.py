from app.Classes import Pallet
from copy import deepcopy


class Customer(object):
    """ A customer object for the sealanes prototype: have the following attributes:

    Attributes:
        id: an unique int identifier to identify a customer with.
        name: a string literal representing the customer's name
        address: a string literal representing the customer's address
    """

    # Constructor
    def __init__(self, customer_id: int, first_name, last_name, full_name, email, address, phone_number,
                 pallets: Pallet):
        """ Return a Customer object."""
        self._customer_id = customer_id
        self._first_name = first_name
        self._last_name = last_name
        self._full_name = full_name
        self._email = email
        self._address = address
        self._phone_number = phone_number
        self._pallets = deepcopy(pallets)

    @property
    def customer_id(self, value: int):
        if value < 0:
            self._customer_id = 0
        else:
            self._customer_id = value

    @customer_id.getter
    def customer_id(self):
        return self._customer_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def full_name(self):
        return '{} {}'.format(self._first_name, self._last_name)

    @property
    def email(self):
        return '{}.{}@email.com'.format(self._first_name, self._last_name)

    @property
    def address(self):
        return '{}'.format(self._address)

    @property
    def phone_number(self):
        return self._phone_number

    @property
    def pallets(self):
        return self._pallets

    @pallets.setter
    def pallets(self, pallets):
        self._pallets = pallets

    # Retrieves the customer's information in a dictionary structure
    def retrieve_information(self):
        return {"Customer ID": self._customer_id,
                "First name": self._first_name,
                "Last name": self._last_name,
                "Full name": self._full_name,
                "E-mail": self._email,
                "Address": self._address,
                "Phone number": self._phone_number,
                "Pallets": self._pallets}

    # Storing the customer's information to "Ask zach" database
    def store_information(self):
        pass