import datetime
import json
import time
from collections import namedtuple

import ccxt
from rich.table import Table

# id to track the trade on the website
# side to track buy and sell
# timestamp to find last fulfilled_trade
# price in quote currency (USDT/ETH)
# size in quote currency (USDT)
# amount = size / price in base currency (ETH)
# filled to see if the order is filled

tradeStruct = namedtuple(
    "tradeStruct", ["id", "side", "timestamp", "price", "amount", "filled", "fee"]
)


class SimpleBot:
    """This bot does the bare minimum"""

    def __init__(self, bot_config, API_JSON):
        self.ccxt = ccxt.kucoin(
            {
                "apiKey": API_JSON["KUCOIN_API_KEY"],
                "secret": API_JSON["KUCOIN_API_SECRET"],
                "password": API_JSON["KUCOIN_PASSWORD"],
                "timeout": 30000,
                # "verbose": True,
                "enableRateLimit": True,
                "rateLimit": 2000,
            },
        )
        self.bot_config = bot_config

        # Variables
        self.n_requests = 0
        self.start_time = time.time()
        self.time_elapsed = 0
        self.stop_buy = False
        self.trades = []
        self.sold_ids = []
        self.referencePrice = 0
        self.targetSellPrice = 0
        self.targetBuyPrice = 0
        self.updateBalance()
        self.updateMarketPrices()
        self.n_buys, self.n_sells = 0, 0
        self.path = self.bot_config["trades_path"]
        self.filename = "trades"
        self.insufficient_balnce = (
            self.balance < self.bot_config["trade_size"] * self.bot_config["max_trades"]
        )
        self.completed_cycles = 0

    def executeBot(self):
        moved = False
        if self.n_buys == 0:
            self.placeTradeOrder("buy", limit=False)
            time.sleep(5)
            updated = self.updateLimitOrders()
            if updated:
                moved = True
            self.updated_last = time.time()
        if time.time() - self.updated_last >= 10:
            updated = self.updateLimitOrders()
            if updated:
                moved = True
            self.updated_last = time.time()
        self.updateMarketPrices()
        self.updateTimeElapsed()

        if self.isBuyTime():
            self.placeTradeOrder("buy", limit=True)
        if self.isSellTime():
            self.placeTradeOrder("sell", limit=True)
        return moved

    def isBuyTime(self):
        return (
            self.market_price
            <= self.targetBuyPrice * (1 + self.bot_config["buy_slippage"])
            and self.balance >= self.bot_config["trade_size"]
            and not self.stop_buy
        )

    def isSellTime(self):
        sell_prices = []
        for trade in self.trades:
            if trade.side == "sell" or not trade.filled or trade.id in self.sold_ids:
                continue
            sell_price = trade.price * (1 + self.bot_config["sell_percent"])
            sell_prices.append(sell_price)
            if self.market_price >= sell_price * (1 - self.bot_config["sell_slippage"]):
                self.sold_ids.append(trade.id)
                self.buy_amount_to_sell = trade.amount
                return True
        try:
            self.targetSellPrice = min(sell_prices)
        except:
            self.targetSellPrice = 9999.9999
        return False

    def placeTradeOrder(self, side, limit=True):
        """Place side (buy/sell) limit order for amount at price."""
        amount = 0.0
        if side == "buy":
            price = self.targetBuyPrice if limit else self.market_price
        else:
            price = self.targetSellPrice if limit else self.market_price
            if not self.bot_config["keep_profits_invested"]:
                amount = self.buy_amount_to_sell
        if amount == 0.0:
            amount = self.bot_config["trade_size"] / price  # in base currency (ETH)
        symbol = self.bot_config["symbol"]

        type = "limit" if limit else "market"
        order = self.ccxt.createOrder(
            symbol=symbol, type=type, side=side, amount=amount, price=price
        )
        trade = tradeStruct(
            id=order["id"],
            side=side,
            timestamp=time.time(),
            price=price,
            amount=amount,
            filled=False,
            fee=None,
        )
        if side == "buy":
            self.n_buys += 1
        else:
            self.n_sells += 1
        self.stop_buy = self.n_buys - self.n_sells >= self.bot_config["max_trades"]
        self.trades.append(trade)
        # print(f"\nUnfilled Trade: {trade}")
        self.saveTrades()
        # self.updateReferencePrice()
        self.referencePrice = price
        self.targetBuyPrice = price * (1 - self.bot_config["buy_percent"])
        self.updateBalance()
        self.n_requests += 1

    def updateLimitOrders(self):
        for i, trade in enumerate(self.trades):
            if trade.filled:
                continue
            order = self.ccxt.fetchOrder(trade.id)
            self.n_requests += 1
            if order["filled"]:
                filled_trade = tradeStruct(
                    id=order["id"],
                    side=trade.side,
                    timestamp=time.time(),
                    price=order["average"],
                    amount=order["amount"],
                    filled=True,
                    fee=order["fee"]["cost"],
                )
                self.trades[i] = filled_trade
                # print(f"\nFilled Trade: {filled_trade}")
                self.saveTrades()
                if trade.side == "sell":
                    self.completed_cycles += 1
                return True
        return False

    def updateMarketPrices(self):
        """Return buy or sell price from latest ticker in exchange ticker"""
        symbol = self.bot_config["symbol"]
        self.market_price = float(self.ccxt.fetchTicker(symbol)["info"]["buy"])
        self.n_requests += 1

    def updateBalance(self):
        self.balance = float(
            self.ccxt.fetchBalance()[self.bot_config["quote_currency"]]["free"]
        )
        self.n_requests += 1

    def saveTrades(self):
        with open(f"{self.path}/{self.filename}.json", "w") as fp:
            json.dump(self.trades, fp, indent=4)
        trades = []
        for trade in self.trades:
            trades.append(list(trade))

    def updateTimeElapsed(self):
        self.time_elapsed = time.time() - self.start_time

    def trades_table(self, text):
        trades_table = Table(title=text["trades_title"], style="blue")
        for column in text["trades_columns"]:
            trades_table.add_column(column, no_wrap=True)
        for trade in self.trades:
            if not trade[5]:
                continue
            id = str(trade[0])
            side = trade[1]
            timestamp = trade[2]
            date = datetime.datetime.fromtimestamp(timestamp).strftime("%A, %B %d, %Y")
            time = datetime.datetime.fromtimestamp(timestamp).strftime("%I:%M:%S %p")
            price = str(trade[3])  # USDT per ETH
            amount = str(trade[4])  # ETH
            fee = str(trade[6])  # USDT
            if side == "buy":
                trades_table.add_row(
                    id, side, date, time, price, amount, fee, style="green"
                )
            else:
                trades_table.add_row(
                    id, side, date, time, price, amount, fee, style="red"
                )
        return trades_table

    def calculate_profits(self):
        stack = []
        profits = 0.0
        for trade in self.trades:
            if not trade[5]:
                continue
            if trade[1] == "buy":
                stack.append(trade)
            else:
                sell_trade = trade
                buy_trade = stack.pop()
                buy_price, sell_price = buy_trade[3], sell_trade[3]
                buy_amount, sell_amount = buy_trade[4], sell_trade[4]
                buy_fee, sell_fee = buy_trade[6], sell_trade[6]
                if not self.bot_config["keep_profits_invested"]:
                    cycle_profit = (sell_price - buy_price) * buy_amount  # USDT
                    cycle_loss = buy_fee + sell_fee
                else:
                    cycle_profit = sell_amount - buy_amount  # ETH
                    cycle_loss = buy_fee / buy_price + sell_fee / sell_price
                profits += cycle_profit - cycle_loss
        return profits

    def market_info(self, text):
        time_elapsed = datetime.timedelta(seconds=round(self.time_elapsed))
        text_market_prices = text["market_price"]
        text_target_prices = text["target_price"]
        text_balance = text["balance"]
        text_stop_buy = text["stop_buy"]
        text_requests = text["requests"]
        text_time_elapsed = text["time_elapsed"]
        buy, sell = text["buy"], text["sell"]
        text_completed_cycles = text["completed_cycles"]
        return (
            "\n"
            f"[bold]{self.bot_config['base_currency']} {text_market_prices}: [/bold]{self.market_price:.2f}\n"
            f"[bold]{self.bot_config['base_currency']} {text_target_prices} ([green]{buy}[/green]/[red]{sell}[/red]): [/bold][green]{self.targetBuyPrice:.2f}[/green]/[red]{self.targetSellPrice:.2f}[/red]\n"
            f"[bold]{text_balance}: [/bold]{self.balance:.2f} {self.bot_config['quote_currency']} \n"
            f"[bold]{text_stop_buy}: [/bold]{self.stop_buy}\n"
            f"[bold]{text_completed_cycles}: [/bold]{self.completed_cycles}"
            f"\n\n[italic]Debugging info:  "
            f"{text_requests}: {self.n_requests} \t {text_time_elapsed}: {time_elapsed}[/italic]"
        )
