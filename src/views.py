import pprint
from typing import Any

from data.config import USER_SETTINGS_JSON
from src.utils import (
    get_greeting,
    get_information_on_card,
    get_top5_transactions,
    get_user_stocks,
    get_user_currencies,
)
from src.utils import get_list_dict_json
import json


def get_json_data(str_datetime: str) -> Any:
    """Функция принимает на вход строку с датой и временем в формате 'YYYY-MM-DD HH:MM:SS',
     и возвращает json-ответ со следующими данными:
     - Приветствие
     - По каждой карте:
       * Последние 4 цифры карты
       * Общая сумма расходов
       * Кэшбэк (1 рубль на каждые 100 рублей)
    - Топ-5 транзакции по сумме платежа
    - Курс акций указанных в user_settings.json
    - Курс валют указанных в user_settings.json
    :param str_datetime
    :return json_data"""

    # приветствие
    greeting = get_greeting()

    # По каждой карте:
    #   Последние 4 цифры карты
    #   Общая сумма расходов
    #   Кэшбэк (1 рубль на каждые 100 рублей)
    information_on_card = get_information_on_card(str_datetime)

    # Топ-5 транзакции по сумме платежа
    top_5_transactions = get_top5_transactions(str_datetime)

    user_setting = get_list_dict_json(USER_SETTINGS_JSON)

    # Курс акций user_settings.json
    user_stocks = user_setting.get("user_stocks")
    list_dict_stock = get_user_stocks(user_stocks)

    # Курс валют user_settings.json
    user_currencies = user_setting.get("user_currencies")
    list_dict_currencies = get_user_currencies(user_currencies)

    result = {
        "greeting": greeting,
        "cards": information_on_card,
        "top_transactions": top_5_transactions,
        "currency_rates": list_dict_currencies,
        "stock_prices": list_dict_stock,
    }
    json_data = json.dumps(result, ensure_ascii=False)

    return json_data


print(json.loads(get_json_data("2021-12-30 06:11:12")))
