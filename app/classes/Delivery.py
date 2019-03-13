class Delivery(object):
    """
         A class that handles the delivery information for a specific pan.
    """

    # A Constructor
    def __init__(self, delivery_id: int, address):
        # creates the variables and initializes it with given variables
        self._delivery_id = delivery_id
        self._address = address

    @property
    def address(self):
        # Returns the address and the id of the delivery
        return '{}'.format(self._address)

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def delivery_id(self, value: int):
        if value < 0:
            self._delivery_id = 0
        else:
            self._delivery_id = value

    @delivery_id.getter
    def delivery_id(self):
        return self._delivery_id

            # Store delivery information ("again as zack")

    # Retrieves the customer's information in a dictionary structure
    def retrieve_information(self):
        return {"Delivery ID": self._delivery_id, "Delivery address": self._address}

    # Store delivery information ("again as zack")
    def store_information(self):
        pass
