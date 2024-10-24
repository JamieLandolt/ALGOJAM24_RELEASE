import numpy as np
import math


# Custom trading Algorithm
class Algorithm():

    ########################################################
    # NO EDITS REQUIRED TO THESE FUNCTIONS
    ########################################################
    # FUNCTION TO SETUP ALGORITHM CLASS
    def __init__(self, positions):
        # Initialise data stores:
        # Historical data of all instruments
        self.data = {}
        # Initialise position limits
        self.positionLimits = {}
        # Initialise the current day as 0
        self.day = 0
        # Initialise the current positions
        self.positions = positions

        self.fintech_recent_prices = []
        self.buying_fintech = False
        self.selling_fintech = False

        self.red_day = None
        self.last_coffee_price = None
        self.milk_mult = 75 / 2000
        self.bean_mult = 7 / 2000

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

        name = [instrument for instrument, positionLimit in positionLimits.items()]
        rank = [name[6], name[2], name[3], name[7], name[4], name[1], name[8], name[5], name[0]]

        self.dailyLimit = 500000

        # Returns number of shares allowed to be transacted according to limitations
        def valid_number_of_shares(instrument):
            if positionLimits[instrument] * self.get_current_price(instrument) <= self.dailyLimit:
                # Update dailylimit
                self.dailyLimit = self.dailyLimit - positionLimits[instrument] * self.get_current_price(instrument)
                # return position
                return positionLimits[instrument]
            elif positionLimits[instrument] * self.get_current_price(instrument) > self.dailyLimit:
                daily_limit = self.dailyLimit
                self.dailyLimit = 0
                return math.floor(daily_limit / self.get_current_price(instrument))

        def buy_long(self, instrument):
            desiredPositions[instrument] = valid_number_of_shares(instrument)

        def sell_long(self, instrument):
            desiredPositions[instrument] = 0

        def buy_short(self, instrument):
            desiredPositions[instrument] = 0

        def sell_short(self, instrument):
            desiredPositions[instrument] = -valid_number_of_shares(instrument)

        def neutralise(self, instrument, desiredPositions):
            if abs(currentPositions[instrument]) <= valid_number_of_shares(instrument):
                desiredPositions[instrument] = 0
            elif abs(currentPositions[instrument]) > valid_number_of_shares(instrument):
                if currentPositions[instrument] > 0:
                    desiredPositions[instrument] = currentPositions[instrument] - valid_number_of_shares(instrument)
                elif currentPositions[instrument] < 0:
                    desiredPositions = currentPositions[instrument] + valid_number_of_shares(instrument)

        # Strategy

        # Sell High, Buy Low
        def sell_high_buy_low(self, instrument):
            if self.day != 0:
                # Price is decreasing
                if self.get_current_price(instrument) < self.data[instrument][-2]:
                    if currentPositions[instrument] < 0:
                        buy_short(self, instrument)
                    buy_long(self, instrument)

                # Price is increasing
                elif self.get_current_price(instrument) > self.data[instrument][-2]:
                    if currentPositions[instrument] > 0:
                        sell_long(self, instrument)
                    sell_short(self, instrument)

        # Growth
        def growth(self, instrument, lower_bound, upper_bound):
            if self.day != 0:
                growth = self.get_current_price(instrument) / self.data[instrument][-2]

                # Growth is below lower_bound
                if growth < lower_bound:
                    if currentPositions[instrument] < 0:
                        buy_short(self, instrument)
                    buy_long(self, instrument)

                # Growth is above upper_bound
                elif growth > upper_bound:
                    if currentPositions[instrument] > 0:
                        sell_long(self, instrument)
                    sell_short(self, instrument)

        # Probability of reversion using M (For UQ Dollars only)
        def probability_of_reversion(self, instrument, M, a):

            probability = abs(1 - abs(self.get_current_price(instrument) - a) / M)

            # probability > 0.5
            if probability > 0.5:

                # If price is below "a"
                if self.get_current_price(instrument) < 100:
                    if currentPositions[instrument] < 0:
                        buy_short(self, instrument)
                    buy_long(self, instrument)

                # If price is above "a"
                elif self.get_current_price(instrument) > 100:
                    if currentPositions[instrument] > 0:
                        sell_long(self, instrument)
                    sell_short(self, instrument)

            # probability < 0.5
            elif probability < 0.5:

                # If price is below "a"
                if self.get_current_price(instrument) < 100:
                    if currentPositions[instrument] > 0:
                        sell_long(self, instrument)
                    sell_short(self, instrument)

                # If price is above "a"
                elif self.get_current_price(instrument) > 100:
                    if currentPositions[instrument] < 0:
                        buy_short(self, instrument)
                    buy_long(self, instrument)

        # Coffee and Milk, trade only coffee
        # def coffee_milk(self):
        #     #Milk is a forward indicator for coffee
        #     growth = self.get_current_price("Milk")/self.data["Milk"][self.day - 1]
        #     if growth > 1:
        #         if currentPositions["Coffee"] < 0:
        #             buy_short(self, "Coffee")
        #         buy_long(self, "Coffee")
        #     elif growth < 1:
        #         if currentPositions["Coffee"] > 0:
        #             sell_long(self, "Coffee")
        #         sell_short(self, "Coffee")

        def get_next_expected_coffee_price(self, milk_price, bean_price, ratio):
            """ Ratio is Milk:Beans"""
            m = int(ratio.split(":")[0])
            b = int(ratio.split(":")[1])
            return self.milk_mult * milk_price * m + self.bean_mult * bean_price * b

        def get_coffee_positions(self, desiredPositions, positionLimits, ratio):
            if self.last_coffee_price is None:
                self.last_coffee_price = self.get_current_price("Coffee")
            next_coffee_price = get_next_expected_coffee_price(self, self.get_current_price("Milk"),
                                                               self.get_current_price("Coffee Beans"),
                                                               ratio)
            if next_coffee_price - self.last_coffee_price > 0:
                desiredPositions["Coffee"] = valid_number_of_shares("Coffee")
            else:
                desiredPositions["Coffee"] = -valid_number_of_shares("Coffee")
            self.last_coffee_price = next_coffee_price

        # Red pens
        def red_pens(self):
            growth = [1]
            for item in range(1, len(self.data["Red Pens"])):
                growth.append(self.data['Red Pens'][item] / self.data['Red Pens'][item - 1])

            # Determine What Day
            for item in range(len(growth)):
                if growth[item] > 1.02337:
                    self.red_day = item - 1
                    while self.day - self.red_day >= 56:
                        self.red_day += 56
                    break

            # if self.day in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
            #     buy_long(self, "Red Pens")
            # elif self.red_day == None:
            #     return
            # elif 15 <= self.day - self.red_day <= 28:
            #     neutralise(self, "Red Pens", desiredPositions)
            # elif 42 <= self.day - self.red_day <= 56:
            #     buy_long(self, "Red Pens")

            if self.red_day == None:
                return
            elif self.day - self.red_day in [0, 7, 14]:
                buy_long(self, "Red Pens")
            elif self.day - self.red_day == 15:
                neutralise(self, "Red Pens", desiredPositions)
            elif (15 < self.day - self.red_day < 27) or (42 < self.day - self.red_day < 55):
                sell_high_buy_low(self, "Red Pens")
            elif self.day - self.red_day in [27, 55]:
                neutralise(self, "Red Pens", desiredPositions)
            elif self.day - self.red_day in [28, 35, 42]:
                sell_short(self, "Red Pens")

            # if self.red_day == None:
            #     return
            # elif self.day - self.red_day in [0]:
            #     buy_long(self, "Red Pens")
            # elif self.day - self.red_day == 15:
            #     neutralise(self, "Red Pens", desiredPositions)
            # elif self.day - self.red_day in [28]:
            #     sell_short(self, "Red Pens")

            # if self.red_day == None:
            #     return
            # elif self.day - self.red_day in [0, 7, 14]:
            #     buy_long(self, "Red Pens")
            # elif self.day - self.red_day in [15, 16, 17]:
            #     sell_long(self, "Red Pens")
            # elif self.day - self.red_day in [28, 35, 42]:
            #     sell_short(self, "Red Pens")
            # elif self.day - self.red_day in [43, 44, 45]:
            #     buy_short(self, "Red Pens")

        def avg(self, l):
            return sum(l) / len(l)

        def update_fintech_recent_prices(self, price):
            for i, val in enumerate(self.fintech_recent_prices[1:]):
                self.fintech_recent_prices[i] = val
            self.fintech_recent_prices[-1] = price

        def get_fintech_positions(self, desiredPositions, positionLimits):
            price = self.get_current_price("Fintech Token")
            if self.day <= 5:
                self.fintech_recent_prices.append(price)
            else:
                update_fintech_recent_prices(self, price)

            recent_avg = avg(self, self.fintech_recent_prices)
            price_change = price - recent_avg

            if self.buying_fintech:
                if price_change < 20:
                    self.buying_fintech = False

            if self.selling_fintech:
                if price_change > -20:
                    self.selling_fintech = False

            if price_change > 45 or self.buying_fintech:
                self.buying_fintech = True
                desiredPositions["Fintech Token"] = valid_number_of_shares("Fintech Token")
                print("BUYING")
            elif price_change < -45 or self.selling_fintech:
                self.selling_fintech = True
                desiredPositions["Fintech Token"] = -valid_number_of_shares("Fintech Token")
                print("Selling")
            else:
                sell_high_buy_low(self, "Fintech Token")
                print("Holding")

        # Call the chosen strategy
        for instrument in rank:
            if instrument == "UQ Dollar":
                probability_of_reversion(self, "UQ Dollar", 0.041, 100)
            elif instrument == "Fun Drink":
                sell_high_buy_low(self, instrument)
            elif instrument == "Coffee":
                # coffee_milk(self)
                get_coffee_positions(self, desiredPositions, positionLimits, ratio="5:3")
            elif instrument == "Fintech Token":
                get_fintech_positions(self, desiredPositions, positionLimits)
            elif instrument == "Red Pens":
                red_pens(self)
            else:
                sell_high_buy_low(self, instrument)


        # growth(self, instrument, 1-0.003, 1+0.003)
        # Fintech sucks
        #red_pens(self)
        #get_fintech_positions(self, desiredPositions, positionLimits)
        #get_coffee_positions(self, desiredPositions, positionLimits, "5:3")


        #######################################################################
        # Return the desired positions
        return desiredPositions