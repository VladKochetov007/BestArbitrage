import time

from BestArbitrage.BestArbitrage import core
from BestArbitrage.BestArbitrage.intra_exchange.bestchain import MinMax


class ArbitrageFinder:
    def __init__(self, client: core.ClientExchangeData):
        self.client = client

    @staticmethod
    def get_profit(alt_base_ask: float, alt_shit_bid: float, shit_base_bid: float) -> float:
        """

        buy  ALT/BASE
        sell ALT/SHIT
        sell SHIT/BASE
        """
        return core.get_percentage(shit_base_bid, alt_base_ask / alt_shit_bid)

    def pare_arbitrage_generator(self,  # no, i can't use itertools.product. i need to check
                                 base=['BTC', 'USDT'],
                                 alt=['XMR', 'XLM'],
                                 shit=['BTC', 'USDT'],
                                 usable_pares=[]):
        alt_base = []
        alt_shit = []
        shit_base = []
        for coin in alt:
            for target in base:
                for market in shit:
                    if coin != target and target != market and market != coin:
                        can = True

                        alba = f"{coin}/{target}"
                        alsh = f"{coin}/{market}"
                        shba = f"{market}/{target}"

                        baal = f"{target}/{coin}"
                        shal = f"{market}/{coin}"
                        bash = f"{target}/{market}"

                        if alba in usable_pares:
                            alba = (alba, 'ask')
                        elif baal in usable_pares:
                            alba = (baal, 'bid')
                        else:
                            can = False

                        if alsh in usable_pares:
                            alsh = (alsh, 'bid')
                        elif shal in usable_pares:
                            alsh = (shal, 'ask')
                        else:
                            can = False

                        if shba in usable_pares:
                            shba = (shba, 'bid')
                        elif bash in usable_pares:
                            shba = (bash, 'ask')
                        else:
                            can = False

                        if can:
                            alt_base.append(alba)
                            alt_shit.append(alsh)
                            shit_base.append(shba)
        self.pares = tuple(zip(alt_base, alt_shit, shit_base))
        return self.pares

    def check(self, coin, target, market) -> MinMax:
        c = self.client.get_price(coin[0], coin[1])
        c1 = c if coin[1] == 'ask' else 1 / c
        t = self.client.get_price(target[0], target[1])
        t1 = t if target[1] == 'bid' else 1 / t
        m = self.client.get_price(market[0], market[1])
        m1 = m if market[1] == 'bid' else 1 / m
        result = self.get_profit(c1, t1, m1)
        return MinMax(coin, target, market, result)

    def start_all_checks(self):
        for pares in self.pares:
            yield self.check(*pares)
