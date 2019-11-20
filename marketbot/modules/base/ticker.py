from marketbot import Bot, Message, util
from discord import Embed, Webhook, TextChannel
from . import api
import re

TICKER_PATTERN = r'\[([a-zA-Z]+)\]'
EXPRESSION_PATTERN = TICKER_PATTERN + r'([.].*)?'


class Stock:
    regex = re.compile(EXPRESSION_PATTERN)
    def __init__(self, ticker):
        self.ticker = ticker

    def default(self):
        e = Embed(title=self.ticker)
        return e

    def test(self, val):
        e = Embed(title="TEST")
        return e





async def manage_stock_object(bot:Bot, message:Message):
    expr = Stock.regex.match(message.content)
    if expr:
        expression = expr.group(0)
        ticker = expr.group(1)
        print(f"expr: {expression}, tkr: {ticker}")
        stock = Stock(ticker)
        expression = expression.replace(f"[{ticker}]", "s", 1)

        try:
            output = eval(expression, {'s':stock})
            channel = bot.get_channel(message.channel.id)  # type: TextChannel
            if isinstance(output, Embed):
                embed = output
            elif isinstance(output, Stock):
                embed = output.default()
            else:
                return
            webhooks = None
            try:
                webhooks = await channel.webhooks()

            except Exception as e:
                print("WH Error:", e)

            if webhooks:
                await webhooks[0].send(embed=embed)
            else:
                await channel.send(embed=embed)

        except Exception as e:
            print("error: ", e)



