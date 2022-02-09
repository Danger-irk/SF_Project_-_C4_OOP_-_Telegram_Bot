import requests
import json
from config import accesse_key, exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, symbol, amount):
        try:
            base.upper() == exchanges[base]
        except KeyError:
            raise APIException(f'Валюта "{base}" не найдена.\n')

        try:
            symbol.upper() == exchanges[symbol]
        except KeyError:
            raise APIException(f'Валюта "{symbol}" не найдена.\n')

        if base == symbol:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}"!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"!\n'
                               f'Третим параметром должно быть число.')

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={accesse_key}")
        response = json.loads(r.content)
        base_rate = float(response["rates"][base])
        symbol_rate = float(response["rates"][symbol])
        new_price = (symbol_rate / base_rate) * float(amount)
        return round(new_price, 4)


class Rate:
    @staticmethod
    def get_rate(name_rate):
        try:
            name_rate.upper() == exchanges[name_rate]
        except KeyError:
            raise APIException(f'Валюта "{name_rate}" не найдена.\n')

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={accesse_key}")
        response = json.loads(r.content)
        rate = float(response["rates"][name_rate])
        rate_rub = float(response["rates"]["RUB"])
        return round((rate_rub / rate), 4)

