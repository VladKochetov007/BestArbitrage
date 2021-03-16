# -*- coding: utf-8 -*-
import re

from colorama import Fore as fore

from BestArbitrage.BestArbitrage.core import get_percentage


class MinMax(object):
    lowerprice_exchange = None
    higherprice_exchange = None
    lowerprice = 0
    higherprice = 0
    percentage_profit = 0

    def __init__(self, loprex='Binance', higprex='Binance', lopr=1, higpr=1, pare=None, loprex_vol=0, higprex_vol=0):
        self.lowerprice_exchange = re.sub(r"[^\w]", '', loprex)
        self.higherprice_exchange = higprex
        self.lowerprice = lopr
        self.higherprice = higpr
        self.loprex_vol = loprex_vol
        self.higprex_vol = higprex_vol
        self.percentage_profit = get_percentage(higpr, lopr)
        self.pare = pare

        if self.percentage_profit < 0.3:
            self.color = fore.LIGHTRED_EX
        elif self.percentage_profit < 1:
            self.color = fore.LIGHTYELLOW_EX
        elif self.percentage_profit < 2:
            self.color = fore.GREEN
        elif self.percentage_profit < 3.4:
            self.color = fore.CYAN
        elif self.percentage_profit < 4.5:
            self.color = fore.BLUE
        else:
            self.color = fore.LIGHTBLUE_EX
        self.data = f"buy {self.pare} at {self.lowerprice_exchange} for {self.lowerprice}, transfer and sell at \
{self.higherprice_exchange} for {self.higherprice} with {round(self.percentage_profit, 2)}% profit (volumes: \
low price: {self.loprex_vol}, high price: {self.higprex_vol})"

    def __repr__(self):
        return f"{self.color}{self.data}{fore.RESET}"
