from BestArbitrage.BestArbitrage import core
from BestArbitrage.BestArbitrage.intra_exchange.bestchain import MinMax
from BestArbitrage.BestArbitrage.intra_exchange import ArbitrageFinder


class Robot(object):
    def __init__(self, client: core.ClientExchangeData = None):
        self.client = client
        self.current_chain: MinMax = MinMax()
        self.finder = ArbitrageFinder(client=client)

    def check_profit(self, chain: MinMax, min_profit=0.15):
        result_chain = self.finder.check(chain.pare1, chain.pare2, chain.pare3)
        return result_chain.profit > min_profit

    def buy_for_all_balance(self, symbol):
        amount = self.client.client.fetch_free_balance()[symbol.split('/')[1]]
        price = self.client.get_price(symbol, 'ask')
        self.client.client.create_market_buy_order(symbol=symbol, amount=amount / price)

    def sell_for_all_balance(self, symbol):
        amount = self.client.client.fetch_free_balance()[symbol.split('/')[0]]
        price = self.client.get_price(symbol, 'bid')
        self.client.client.create_market_sell_order(symbol=symbol, amount=amount)

    def run_buy_sell_order(self, pare=('BTC/USDT', 'ask')):
        if pare[1] == 'ask':
            self.buy_for_all_balance(pare[0])
        else:
            self.sell_for_all_balance(pare[0])

    def execute_chain(self, chain: MinMax):
        orders = chain.pare1, chain.pare2, chain.pare3
        for order in orders:
            self.run_buy_sell_order(order)

    @staticmethod
    def get_best_chain(chains):
        tune = lambda ch: ch.profit
        return max(chains, key=tune)

    def find_chain(self, min_profit=0.15, parallel=False, sleep=0):
        if self.current_chain is not None:
            is_ok = self.check_profit(self.current_chain, min_profit=min_profit)
        else:
            is_ok = False

        if is_ok:
            return self.current_chain
        else:
            # finding best chain
            tickers = self.client.client.fetch_tickers()
            asset1 = list(set(map(lambda x: x.split('/')[0], list(tickers.keys()))))
            enable_pares = list(tickers.keys())
            pares = self.finder.pare_arbitrage_generator(alt=asset1, usable_pares=enable_pares)
            chains = list(self.finder.start_all_checks(sleep=sleep, parallel=parallel))
            best = self.get_best_chain(chains=chains)
            return best

    def start_arbitrage(self):




if __name__ == '__main__':
    import ccxt
    print(Robot(core.ClientExchangeData(client=ccxt.poloniex())).check_profit(
    MinMax(('DMG/USDT', 'ask'), ('DMG/BTC', 'bid'), ('BTC/USDT', 'bid'))
     ))
