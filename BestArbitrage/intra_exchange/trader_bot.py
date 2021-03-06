import time

from BestArbitrage.BestArbitrage import core
from BestArbitrage.BestArbitrage.intra_exchange.bestchain import MinMax
from BestArbitrage.BestArbitrage.intra_exchange.parser import ArbitrageFinder


class Robot(object):
    def __init__(self, client: core.ClientExchangeData = None):
        self.client = client
        self.current_chain: MinMax = None
        self.finder = ArbitrageFinder(client=client)

    def check_profit(self, chain: MinMax, min_profit=0.15):
        result_chain = self.finder.check(chain.pare1, chain.pare2, chain.pare3)
        return result_chain.profit > min_profit

    def buy_for_all_balance(self, symbol):
        if core._test:
            print(f"buy {symbol}")
        else:
            amount = self.client.client.fetch_free_balance()[symbol.split('/')[1]]
            price = self.client.get_price(symbol, 'ask')
            self.client.client.create_market_buy_order(symbol=symbol, amount=amount / price)

    def sell_for_all_balance(self, symbol):
        if core._test:
            print(f"sell {symbol}")
        else:
            amount = self.client.client.fetch_free_balance()[symbol.split('/')[0]]
            price = self.client.get_price(symbol, 'bid')
            self.client.client.create_market_sell_order(symbol=symbol, amount=amount)

    def run_buy_sell_order(self, pare=('BTC/USDT', 'ask')):
        if pare[1] == 'ask':
            self.buy_for_all_balance(pare[0])
        else:
            self.sell_for_all_balance(pare[0])

    def execute_chain(self, chain: MinMax, sleep_in_deals=0):
        orders = chain.pare1, chain.pare2, chain.pare3
        for e, order in enumerate(orders, 1):
            self.run_buy_sell_order(order)
            if e != 3 and sleep_in_deals:
                time.sleep(sleep_in_deals)

    @staticmethod
    def _get_best_chain(chains):
        tune = lambda ch: ch.profit
        return max(chains, key=tune)

    def find_chain(self, min_profit=0.15, parallel=False, sleep=0):
        if self.current_chain is not None:
            is_ok = self.check_profit(self.current_chain, min_profit=min_profit)
        else:
            is_ok = False

        if is_ok:
            return self.current_chain
        else:  # finding best chain
            tickers = self.client.client.fetch_tickers()
            asset1 = list(set(map(lambda x: x.split('/')[0], list(tickers.keys()))))
            enable_pares = list(tickers.keys())
            pares = self.finder.pare_arbitrage_generator(alt=asset1, usable_pares=enable_pares)
            chains = list(self.finder.start_all_checks(sleep=sleep, parallel=parallel))
            best = self._get_best_chain(chains=chains)
            self.current_chain = best
            return best

    def start_arbitrage(self, min_profit=0.15, parallel=False, sleep_in_api=0, sleep_in_chains=0, sleep_in_deals=0):
        while True:
            self.execute_chain(
                self.find_chain(
                    min_profit=min_profit,
                    parallel=parallel,
                    sleep=sleep_in_api
                ),
                sleep_in_deals=sleep_in_deals
            )
            time.sleep(sleep_in_chains)


if __name__ == '__main__':
    import ccxt

    robot = Robot(core.ClientExchangeData(client=ccxt.poloniex()))
    print(robot.finder.check(
        ('DMG/USDT', 'ask'), ('DMG/BTC', 'bid'), ('BTC/USDT', 'bid'))
    )
    robot = Robot(core.ClientExchangeData(client=ccxt.kucoin()))
    print(robot.finder.check(
        ('BRG/USDT', 'ask'), ('BRG/BTC', 'bid'), ('BTC/USDT', 'bid'))
    )
