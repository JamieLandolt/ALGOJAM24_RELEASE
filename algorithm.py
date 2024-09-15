from matplotlib import pyplot as plt


class Algorithm():

    ########################################################
    # NO EDITS REQUIRED TO THESE FUNCTIONS
    ########################################################
    # FUNCTION TO SETUP ALGORITHM CLASS
    def __init__(self, positions):
        # Initialise data stores:
        # Historical data of all instruments
        self.data = {}
        self.milk_mult = 75 / 2000 * 6
        self.bean_mult = 7 / 2000
        self.c = 0
        # Initialise position limits
        self.positionLimits = {}
        # Initialise the current day as 0
        self.day = 0
        # Initialise the current positions
        self.positions = positions
        self.last_coffee_price = None
        self.fintech_recent_prices = []
        self.buying_fintech = False
        self.selling_fintech = False

    # Helper function to fetch the current price of an instrument
    def get_current_price(self, instrument):
        # return most recent price
        return self.data[instrument][-1]

    ########################################################

    # RETURN DESIRED POSITIONS IN DICT FORM
    def get_positions(self):
        # Get current position
        currentPositions = self.positions
        # Get position limits
        positionLimits = self.positionLimits

        # Declare a store for desired positions
        desiredPositions = {}
        # Loop through all the instruments you can take positions on.
        for instrument, positionLimit in positionLimits.items():
            # For each instrument initilise desired position to zero
            desiredPositions[instrument] = 0

        # IMPLEMENT CODE HERE TO DECIDE WHAT POSITIONS YOU WANT
        #######################################################################
        # Buy thrifted jeans maximum amount

        """current_thrifted = self.get_current_price("Thrifted Jeans")
        next_expected_thrifted_price = self.get_expected_thrifted_price(self.day + 1)
        print(current_thrifted)
        print(next_expected_thrifted_price)
        if next_expected_thrifted_price - current_thrifted > 0:
            desiredPositions["Thrifted Jeans"] = positionLimits["Thrifted Jeans"]
        else:
            desiredPositions["Thrifted Jeans"] = -positionLimits["Thrifted Jeans"]"""

        #self.get_coffee_positions(desiredPositions, positionLimits, ratio="1:3")
        # self.get_fintech_positions(desiredPositions, positionLimits)

        #######################################################################
        # Return the desired positions
        return desiredPositions

    def avg(self, l):
        return sum(l) / len(l)

    def read_csv(self, csv, val_type=float):
        with open(csv) as ft:
            d = {}
            for i, line in enumerate(ft):
                if i != 0:
                    line = line.split(",")
                    for c, val in enumerate(line):
                        if c not in d:
                            d[c] = [val_type(val.strip())]
                        else:
                            d[c].append(val_type(val.strip()))
            return tuple(i for i in d.values())

    def get_expected_thrifted_price(self, day):
        if day < 366:
            # Prediction Equation: val = 0.09003603892119379(day) + 69.80511709601876
            return 0.06121634425160155 * day + 47.4611514441842
        else:
            return 0.09003603892119379 * day + 69.80511709601876

    def get_next_expected_coffee_price(self, milk_price, bean_price, ratio):
        """ Ratio is Milk:Beans"""
        m = int(ratio.split(":")[0])
        b = int(ratio.split(":")[1])
        return self.milk_mult * milk_price * m + self.bean_mult * bean_price * b

    def update_fintech_recent_prices(self, price):
        for i, val in enumerate(self.fintech_recent_prices[1:]):
            self.fintech_recent_prices[i] = val
        self.fintech_recent_prices[-1] = price

    def get_fintech_positions(self, desiredPositions, positionLimits):
        price = self.get_current_price("Fintech Token")
        if self.day <= 5:
            self.fintech_recent_prices.append(price)
        else:
            self.update_fintech_recent_prices(price)

        recent_avg = self.avg(self.fintech_recent_prices)
        price_change = price - recent_avg

        if self.buying_fintech:
            if price_change < 20:
                self.buying_fintech = False

        if self.selling_fintech:
            if price_change > -20:
                self.selling_fintech = False

        if price_change > 45 or self.buying_fintech:
            self.buying_fintech = True
            desiredPositions["Fintech Token"] = positionLimits["Fintech Token"]
            print("BUYING")
        elif price_change < -45 or self.selling_fintech:
            self.selling_fintech = True
            desiredPositions["Fintech Token"] = -positionLimits["Fintech Token"]
            print("Selling")
        else:
            # TODO Implement Tom's Buy High Sell Low here for the average holding price
            desiredPositions["Fintech Token"] = 0
            print("Holding")

    def get_coffee_positions(self, desiredPositions, positionLimits, ratio):
        if self.last_coffee_price is None:
            self.last_coffee_price = self.get_current_price("Coffee")
        next_coffee_price = self.get_next_expected_coffee_price(self.get_current_price("Milk"),
                                                                self.get_current_price("Coffee Beans"),
                                                                ratio)
        print(f"{next_coffee_price=}")
        if next_coffee_price - self.last_coffee_price > 0:
            desiredPositions["Coffee"] = positionLimits["Coffee"]
            self.c += 1
        else:
            desiredPositions["Coffee"] = -positionLimits["Coffee"]
            self.c -= 1
        print(self.c)
        self.last_coffee_price = next_coffee_price

    def graph_csv(self, csv):
        x, y = self.read_csv(csv)
        plt.clf()
        plt.plot(x, y, label="Fun Drink")
        plt.show()

a = Algorithm(1)
a.graph_csv("data/Fun Drink_price_history.csv")