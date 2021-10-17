import time

from BestArbitrage.BestArbitrage import core
from BestArbitrage.BestArbitrage.intra_exchange.bestchain import MinMax
from BestArbitrage.BestArbitrage.intra_exchange.parser import ArbitrageFinder


class Robot(object):
    def __init__(self, client: core.Client = None, quote_in_account='USDT', use_quote_only=False):
        self.current_chain: MinMax = None
        self.finder = ArbitrageFinder(client=client)
        self.current_quote = quote_in_account
        self.enable_pairs = list(client.client.fetch_tickers().keys())
        self.use_only_quote = use_quote_only

    def check_profit(self, min_profit=0.4):
        chain = self.current_chain
        self.current_chain = self.finder.check(chain.pair1, chain.pair2, chain.pair3)
        return self.current_chain.profit >= min_profit

    def buy_for_all_balance(self, symbol):
        if core._VERBOSE:
            print(f"buy {symbol}")
        if not core._TEST:
            amount = self.finder.client.client.fetch_free_balance()[symbol.split('/')[1]]
            price = self.finder.client.get_price(symbol, 'ask')
            self.finder.client.client.create_order(
                symbol=symbol,
                type='market',
                side='buy',
                amount=amount / price,
                price=price
            )

    def sell_for_all_balance(self, symbol):
        if core._VERBOSE:
            print(f"sell {symbol}")
        if not core._TEST:
            amount = self.finder.client.client.fetch_free_balance()[symbol.split('/')[0]]
            price = self.finder.client.get_price(symbol, 'bid')
            self.finder.client.client.create_order(
                symbol=symbol,
                type='market',
                side='sell',
                amount=amount,
                price=price
            )

    def run_buy_sell_order(self, pair=('BTC/USDT', 'ask')):
        if core._VERBOSE:
            print(pair)
        if pair[1] == 'ask':
            self.buy_for_all_balance(pair[0])
        else:
            self.sell_for_all_balance(pair[0])

    def execute_chain(self, sleep_in_deals=0):
        orders = (self.current_chain.pair1,
                  self.current_chain.pair2,
                  self.current_chain.pair3)
        for e, order in enumerate(orders, 1):
            self.run_buy_sell_order(order)
            if e != 3 and sleep_in_deals:
                time.sleep(sleep_in_deals)

    @staticmethod
    def _get_best_chain(chains) -> MinMax:
        tune = lambda ch: ch.profit
        return max(chains, key=tune)

    def find_chain(self, min_profit=0.5):
        self.finder.client.update_tickers()
        chains = list(self.finder.start_all_checks())
        best = self._get_best_chain(chains=chains)
        if best.profit >= min_profit:
            self.current_chain = best
        else:
            self.current_chain = None
        if core._VERBOSE:
            print(best)
        return self.current_chain

    def start_arbitrage(self,
                        min_profit=0.4,
                        sleep_in_chains=0,
                        sleep_in_deals=0):
        asset1 = list(set(
            map(lambda x: x.split('/')[0], self.enable_pairs)
        ))
        self.finder.pair_arbitrage_generator(
            alt=asset1,
            usable_pairs=self.enable_pairs
        )
        while True:
            self.find_chain(min_profit=min_profit)
            if self.current_chain is not None:
                if (not self.use_only_quote) or self.current_quote == self.current_chain.get_needed_coin():
                    self.prepare_to_chain()
                    self.execute_chain(sleep_in_deals=sleep_in_deals)
            time.sleep(sleep_in_chains)

    def prepare_to_chain(self):
        coin = self.current_chain.get_needed_coin()
        if coin != self.current_quote:
            symbol = f"{coin}/{self.current_quote}"
            if symbol not in self.enable_pairs:
                self.sell_for_all_balance(f"{self.current_quote}/{coin}")
            else:
                self.buy_for_all_balance(symbol)
            self.current_quote = coin
