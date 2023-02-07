import asyncio
import aiohttp
from time import time


log = open("log.txt", "w")
exchangers: list
pairs_binance: dict
pairs_binance: dict
pairs_huobi: dict
pairs_bybit: dict
pairs_kucoin: dict
pairs_mexc: dict
# pairs_bilaxy: dict
pairs_hitbtc: dict
pairs_ascendex: dict
main_set: set

loopl = asyncio.get_event_loop()
loopd = asyncio.get_event_loop()
session: aiohttp.ClientSession


class Direction:
    r = 0
    l = 1
    b = 2
    n = 3


async def binance():
    url_binance = 'https://api.binance.com/api/v3/exchangeInfo'
    url_binance_max_min_info = 'https://api.binance.com/api/v3/ticker/bookTicker'
    try:
        async with session.get(url_binance) as data:
            r = await data.json()
            for symbol in r['symbols']:
                if symbol["status"] == "TRADING" and "SPOT" in symbol["permissions"]:
                    name = symbol["symbol"]
                    pairs_binance[name] = [symbol["baseAsset"], symbol["quoteAsset"]]
        async with session.get(url_binance_max_min_info) as data:
            r = await data.json()
            for sym in r:
                symbol = sym["symbol"]
                tmp = pairs_binance.get(symbol)
                if tmp:
                    bid, ask = sym["bidPrice"], sym["askPrice"]
                    if not bid:
                        if not ask:
                            del pairs_binance[symbol]
                            continue
                        else:
                            pairs_binance[symbol] = tmp + [-1e100, ask, Direction.n]
                    else:
                        pairs_binance[symbol] = tmp + [bid, 1e100 if not ask else ask, Direction.n]
                    main_set.add(symbol)
    except:
        log.write(f"===============Our IP fully banned by BINANCE===============\n")
