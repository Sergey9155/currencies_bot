import requests
import json
from config import keys


class APIException(Exception):
    ...


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amoute: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты{base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amoute = float(amoute)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amoute}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amoute
