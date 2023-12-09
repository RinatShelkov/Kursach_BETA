import datetime

import numpy as np
import pandas as pd
import pytest

from data.config import TEST_OPERATIONS_XLS
from src.reports import spending_by_category


@pytest.fixture
def transaction():
    transaction_ = TEST_OPERATIONS_XLS
    return transaction_


@pytest.fixture
def category():
    category_ = "Супермаркеты"
    return category_


@pytest.fixture
def date():
    date_ = "2021-12-28 06:11:12"
    return date_


@pytest.fixture
def df_true():
    df_true_ = [
        {
            "Дата операции": "27.12.2021 12:01:09",
            "Дата платежа": "27.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -40.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -40.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Evo_Lyzhnyj",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 40.0,
        }
    ]
    df_true_ = pd.DataFrame(df_true_)
    df_true_["Дата операции"] = df_true_["Дата операции"].apply(
        lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M:%S")
    )
    df_true_.rename(columns={"Дата операции": "date"}, inplace=True)
    df_true_["Кэшбэк"] = df_true_["Кэшбэк"].apply(lambda x: np.float64(x))
    return df_true_


def test_spending_by_category(transaction, category, date, df_true):
    df_func = spending_by_category(transaction, category, date)
    df_true_ = df_true
    pd.testing.assert_frame_equal(df_true_, df_func)


def test_spending_by_category_not_date(transaction, category):
    df_func = spending_by_category(transaction, category)
    df_true_ = pd.DataFrame([])
    pd.testing.assert_frame_equal(df_true_, df_func)
