import json
import requests
from config import exchanger


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise APIException("Недопустимый формат ввода")
        quote, base, amount = values
        if quote == base:
            raise APIException(f"Невозможно перевести {base} в {base}")        
        try:
            base_ticket = exchanger[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")
        try:
            quote_ticket = exchanger[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        r = requests.get(f'https://belarusbank.by/api/kursExchange?')
        total = json.loads(r.content)[0]     
        text_request = f"{exchanger[quote]}_{exchanger[base]}_in"
        if text_request == "EUR_RUB_in" or "RUB_USD_in" == text_request or "EUR_USD_in" == text_request:
            total = 1 / float(total[f"{exchanger[base]}_{exchanger[quote]}_in"]) * float(amount)
        else:
            total = float(total[text_request]) * float(amount)        
        return round(total, 2)
