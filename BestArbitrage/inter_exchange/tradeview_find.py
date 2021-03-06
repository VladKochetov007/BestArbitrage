# -*- coding: utf-8 -*-

from selenium.common.exceptions import InvalidSessionIdException

import BestArbitrage.BestArbitrage.inter_exchange.bestexchange as bestexchange
from BestArbitrage.BestArbitrage import core


class ArbitrageFounder(core.AskTradingView):

    def get_data(
            self,
            pare,
            your_exchanges=[
                "BINANCE",
                "FTX"
            ],
            exchange_blacklist=["BITTREX", "CAPITALCOM", "CURRENCYCOM"],
            all_exchanges=True,
            min_volumes={
                'BTC': 0.25,
                'ETH': 5,
                'USDT': 10000
            },
            print_oops=True):
        try:
            exc_pare = {}
            self.driver.get(f"https://ru.tradingview.com/symbols/{pare}/markets/")
            exchanges = self.driver.find_elements_by_class_name(
                "tv-data-table__row.tv-data-table__stroke.tv-screener-table__result-row"
            )
            for item in exchanges:
                item_call = item.find_elements_by_class_name(
                    "tv-data-table__cell.tv-screener-table__cell"
                )
                exchange = item_call[0].text
                volume = item_call[6].text

                if volume[-1] == "K":
                    vol = float(volume[:-1]) * 1_000
                elif volume[-1] == "M":
                    vol = float(volume[:-1]) * 1_000_000
                elif volume[-1] == "B":
                    vol = float(volume[:-1]) * 1_000_000_000
                else:
                    vol = float(volume)

                price = float(item_call[1].text)
                for key, val in zip(min_volumes.keys(),
                                    min_volumes.values()):
                    if pare.endswith(key):
                        min_vol_ = val
                if (
                        exchange in your_exchanges or all_exchanges) and vol >= min_vol_ and exchange not in exchange_blacklist:
                    exc_pare[exchange] = {"volume": vol,
                                          "price": price}
            if len(list(exc_pare.keys())) == 0:
                return None
            list_exchanges = []
            for exchange in exc_pare.keys():
                price = exc_pare[exchange]["price"]
                list_exchanges.append({exchange: price})
            get_sort = lambda x: list(x.values())[0]
            get_sort_key = lambda x: list(x.keys())[0]
            minimal = min(list_exchanges, key=get_sort)
            maximal = max(list_exchanges, key=get_sort)
            return bestexchange.MinMax(
                get_sort_key(minimal),
                get_sort_key(maximal),
                get_sort(minimal),
                get_sort(maximal),
                pare=pare,
                higprex_vol=exc_pare[get_sort_key(maximal)]['volume'],
                loprex_vol=exc_pare[get_sort_key(minimal)]['volume']
            )
        except Exception as e:
            if isinstance(e, (KeyboardInterrupt, InvalidSessionIdException)):
                raise e
            if print_oops:
                print('Oops, something went wrong...')
            return None
