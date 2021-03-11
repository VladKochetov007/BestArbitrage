import time

from BestArbitrage.BestArbitrage import core
from BestArbitrage.BestArbitrage.intra_exchange.bestchain import MinMax
from BestArbitrage.BestArbitrage.intra_exchange.parser import ArbitrageFinder


class Robot(object):
    def __init__(self, client: core.ClientExchangeData = None, quote_in_account='USDT', use_quote_only=False):
        self.client = client
        # noinspection PyTypeChecker
        self.current_chain: MinMax = None
        self.finder = ArbitrageFinder(client=client)
        self.current_quote = quote_in_account
        self.enable_pares = list(client.client.fetch_tickers().keys())
        self.use_only_quote = use_quote_only

    def check_profit(self, min_profit=0.4):
        chain = self.current_chain
        self.current_chain = self.finder.check(chain.pare1, chain.pare2, chain.pare3)
        return self.current_chain.profit >= min_profit

    def buy_for_all_balance(self, symbol):
        if core._VERBOSE:
            print(f"buy {symbol}")
        if not core._TEST:
            amount = self.client.client.fetch_free_balance()[symbol.split('/')[1]]
            price = self.client.get_price(symbol, 'ask')
            self.client.client.create_order(
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
            amount = self.client.client.fetch_free_balance()[symbol.split('/')[0]]
            price = self.client.get_price(symbol, 'bid')
            self.client.client.create_order(
                symbol=symbol,
                type='market',
                side='sell',
                amount=amount,
                price=price
            )

    def run_buy_sell_order(self, pare=('BTC/USDT', 'ask')):
        if pare[1] == 'ask':
            self.buy_for_all_balance(pare[0])
        else:
            self.sell_for_all_balance(pare[0])

    def execute_chain(self, sleep_in_deals=0, print_attention=True):
        orders = self.current_chain.pare1, self.current_chain.pare2, self.current_chain.pare3
        for e, order in enumerate(orders, 1):
            self.run_buy_sell_order(order)
            if e != 3 and sleep_in_deals:
                time.sleep(sleep_in_deals)

    @staticmethod
    def _get_best_chain(chains) -> MinMax:
        tune = lambda ch: ch.profit
        return max(chains, key=tune)

    def find_chain(self, min_profit=0.5):
        self.client.update_tickers()
        if self.current_chain is not None:
            is_ok = self.check_profit(min_profit=min_profit)
        else:
            is_ok = False

        if is_ok:
            if core._VERBOSE:
                print(self.current_chain)
            return self.current_chain
        else:  # finding best chain
            asset1 = list(set(
                map(lambda x: x.split('/')[0], self.enable_pares)
            ))
            pares = self.finder.pare_arbitrage_generator(alt=asset1, usable_pares=self.enable_pares)
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
                        sleep_in_deals=0,
                        print_attention=True):
        while True:
            self.find_chain(
                min_profit=min_profit
            )
            if (not self.use_only_quote) or self.current_quote == self.current_chain.get_needed_coin():
                quote_can_use = True
            else:
                quote_can_use = False
            if self.current_chain is not None and quote_can_use:
                self.prepare_to_chain()
                self.execute_chain(
                    sleep_in_deals=sleep_in_deals,
                    print_attention=print_attention
                )

            time.sleep(sleep_in_chains)

    def prepare_to_chain(self):
        coin = self.current_chain.get_needed_coin()
        if coin != self.current_quote:
            symbol = f"{coin}/{self.current_quote}"
            if symbol not in self.enable_pares:
                self.sell_for_all_balance(f"{self.current_quote}/{coin}")
            else:
                self.buy_for_all_balance(symbol)
            self.current_quote = coin
