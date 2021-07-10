import os
import json
from finnhub import Finnhub
from marketstack import Marketstack

if __name__ == "__main__":
    fh_token = os.environ.get("FINNHUB_TOKEN")
    if fh_token:
        fh = Finnhub(token=fh_token)
        res = fh.get_quote("BNP.PA")
        print(json.dumps(res))

    ms_token = os.environ.get("MARKETSTACK_TOKEN")
    if ms_token:
        ms = Marketstack(token=ms_token)
        # res = ms.get_quote("BNP.XPAR")
        # print(json.dumps(res))
        res = ms.get_quotes(["BNP.XPAR", "TSLA"])
        print(json.dumps(res))
