# -*- coding: utf-8 -*-
from typing import Tuple

from colorama import Fore


class MinMax(object):
    def __init__(self,
                 pare1: Tuple[str, str] = ('None', 'ask'),
                 pare2: Tuple[str, str] = ('None', 'bid'),
                 pare3: Tuple[str, str] = ('None', 'bid'),
                 profit=0):
        self.pare1 = pare1
        self.pare2 = pare2
        self.pare3 = pare3
        self.profit = profit

        if pare1[1] == 'ask':
            BS1 = f"buy {pare1[0]}"
        else:
            BS1 = f"sell {pare1[0]}"

        if pare2[1] == 'ask':
            BS2 = f"buy {pare2[0]}"
        else:
            BS2 = f"sell {pare2[0]}"

        if pare3[1] == 'ask':
            BS3 = f"buy {pare3[0]}"
        else:
            BS3 = f"sell {pare3[0]}"
        self.data = f"{BS1}, {BS2}, {BS3} with {round(self.profit, 3)}% profit"

        if profit <= 0:
            self.color = Fore.BLACK
        elif profit < 0.03:
            self.color = Fore.LIGHTRED_EX
        elif profit < 0.1:
            self.color = Fore.LIGHTYELLOW_EX
        elif profit < 0.2:
            self.color = Fore.GREEN
        elif profit < 0.34:
            self.color = Fore.CYAN
        elif profit < 0.45:
            self.color = Fore.BLUE
        else:
            self.color = Fore.LIGHTBLUE_EX

    def __repr__(self):
        return f"{self.color}{self.data}{Fore.RESET}"

    def get_needed_coin(self):
        get = lambda x: self.pare1[0].split('/')[x]
        if self.pare1[1] == 'ask':
            return get(1)
        else:
            return get(0)
