# -*- coding: utf-8 -*-
import re

from colorama import Fore as fore

from BestArbitrage.BestArbitrage.core import get_percentage


class MinMax(object):
    lower_price_exchange = None
    higher_price_exchange = None
    lower_price = 0
    higher_price = 0
    percentage_profit = 0
    pair: str

    def __init__(self,
                 lower_price_exchange='Binance',
                 higher_price_exchange='Binance',
                 lower_price=1,
                 higher_price=1,
                 pair=None,
                 lower_price_volume=0,
                 higher_price_volume=0):
        self.lower_price_exchange = re.sub(r"[^\w]", '', lower_price_exchange)
        self.higher_price_exchange = higher_price_exchange
        self.lower_price = lower_price
        self.higher_price = higher_price
        self.lower_price_volume = lower_price_volume
        self.higher_price_volume = higher_price_volume
        self.percentage_profit = get_percentage(higher_price, lower_price)
        self.pair = pair

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
        self.data = f"buy {self.pair} at {self.lower_price_exchange} for {self.lower_price}, transfer and sell at \
{self.higher_price_exchange} for {self.higher_price} with {round(self.percentage_profit, 2)}% profit (volumes: \
low price: {self.lower_price_volume}, high price: {self.higher_price_volume})"

    def __repr__(self):
        return f"{self.color}{self.data}{fore.RESET}"
