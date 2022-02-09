import requests
import json
from config import accesse_key, exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, symbol, amount):
        try:
            base == exchanges[base.upper()]
        except KeyError:
            raise APIException(f'Валюта "{base}" не найдена.\n'
                               f'Проверьте обозначение валют по команде - /values')

        try:
            symbol == exchanges[symbol.upper()]
        except KeyError:
            raise APIException(f'Валюта "{symbol}" не найдена.\n'
                               f'Проверьте обозначение валют по команде - /values')

        if base == symbol:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}"!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"!\n'
                               f'Третим параметром должно быть число.')

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={accesse_key}")
        response = json.loads(r.content)
        base_rates = float(response["rates"][base])
        symbol_rates = float(response["rates"][symbol])
        new_price = (symbol_rates / base_rates) * float(amount)
        return round(new_price, 4)
