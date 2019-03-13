class Contents(object):
    """
        A class that handles the Contents type
    """

    # A Constructor/Initializer
    def __init__(self, quantity: int, name):
        # creates class variables
        self._name = name
        self._quantity = quantity

    # To retrieve the Contents information
    def retrieve_contents(self):
        # Returns the Contents information
        return {"Name": self._name, "Quantity": self._quantity}

    # To store the Contents to the ("Ask zack") database
    def store_Contents(self):
        pass
