import pprint
from typing import Any

from data.config import USER_SETTINGS_JSON
from src.utils import get_greeting, get_information_on_card, get_top5_transactions, \
    get_user_stocks, get_user_currencies
from src.utils import get_list_dict_json


def get_json_data(str_datetime: str) -> Any:
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
    user_stocks = user_setting.get('user_stocks')
    # list_dict_stock = get_user_stocks(user_stocks)

    # Курс валют user_settings.json
    user_currencies = user_setting.get('user_currencies')
    list_dict_currencies = get_user_currencies(user_currencies)

    return greeting, information_on_card, top_5_transactions, user_stocks, list_dict_currencies


pprint.pprint(get_json_data('2021-08-30 06:11:12'))
