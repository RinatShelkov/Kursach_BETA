import pytest

from src.services import simple_search


def test_simple_search():
    assert simple_search("Линзомат ТЦ Юность") == (
        '[{"Дата операции": "01.01.2018 12:49:53", "Дата платежа": "01.01.2018", '
        '"Номер карты": null, "Статус": "OK", "Сумма операции": -3000.0, "Валюта '
        'операции": "RUB", "Сумма платежа": -3000.0, "Валюта платежа": "RUB", '
        '"Кэшбэк": NaN, "Категория": "Переводы", "MCC": NaN, "Описание": "Линзомат ТЦ '
        'Юность", "Бонусы (включая кэшбэк)": 0, "Округление на инвесткопилку": 0, '
        '"Сумма операции с округлением": 3000.0}]'
    )
