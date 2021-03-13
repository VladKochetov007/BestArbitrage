import re

import ccxt
import selenium.webdriver.support.expected_conditions as ec
from numpy import inf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

_TEST = False
_VERBOSE = False


def get_percentage(higherprice, lowerprice):
    increace = higherprice - lowerprice
    if lowerprice == 0:
        percentage_profit = inf
    else:
        percentage_profit = (increace / lowerprice) * 100
    return percentage_profit


class ClientExchangeData(object):
    def __init__(self, client: ccxt.Exchange = None):
        self.client = client
        if self.client is not None:
            self.update_tickers()

    def update_tickers(self):
        self._fetch_tickers = self.client.fetch_tickers()

    def get_price(self, symbol, side='ask/bid'):
        ticker = self._fetch_tickers[symbol]
        if side == "ask":
            return float(ticker['ask'])
        else:
            return float(ticker['bid'])


class AskTradingView(object):
    def __init__(self, driver=None):
        self.driver: webdriver.Safari = driver

    def get_all_tv_pares(self, screener='crypto-screener'):
        self.driver.get(f"https://ru.tradingview.com/{screener}/")

        waiter = WebDriverWait(self.driver, 5)
        items = waiter.until(ec.visibility_of_all_elements_located(
            (By.CLASS_NAME, "tv-screener__symbol.apply-common-tooltip")))
        return set(map(lambda x: x.text, items))

    def get_all_coins(self, screener='cryptocurrencies', pages=3):
        self.driver.get(f"https://ru.tradingview.com/markets/{screener}/prices-all/")

        waiter = WebDriverWait(self.driver, 5)
        items = []
        loadmore = self.driver.find_element_by_class_name("tv-load-more__btn")
        for page in range(pages):
            items.extend(
                waiter.until(
                    ec.visibility_of_all_elements_located(
                        (By.CLASS_NAME,
                         "tv-data-table__row.tv-data-table__stroke."
                         "tv-screener-table__result-row")
                    )
                )
            )
            loadmore.click()

        cryptos = list(
            map(
                lambda x: re.findall(
                    r":.+",
                    x.get_attribute('data-symbol')
                )[0][1:-3],
                items
            )
        )
        return cryptos
