import datetime
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import HTTPError

from data.config import (
    TEST_TRANSACTION_PATH_CSV,
    TEST_TRANSACTION_PATH_XLSX,
    USER_SETTINGS_JSON,
    TEST_UTILS_FileNotFoundError,
    TEST_UTILS_JSONDecodeError,
    TEST_READING_JSON,
    TEST_USER_SETTINGS_JSON,
)
from src.utils import (
    get_greeting,
    get_information_on_card,
    reading_csv_xlsx_file,
    get_list_dict_json,
    get_top5_transactions,
    get_user_stocks,
    get_user_currencies,
)


def test_reading_xlsx_file():
    with patch("src.utils.reading_csv_xlsx_file") as mock_get:
        mock_get(TEST_TRANSACTION_PATH_XLSX).return_value = 650703.0

        assert reading_csv_xlsx_file(TEST_TRANSACTION_PATH_XLSX)[0]["id"] == 650703.0
        mock_get.assert_called_once_with(TEST_TRANSACTION_PATH_XLSX)


def test_reading_csv_file():
    with patch("src.utils.reading_csv_xlsx_file") as mock_get:
        mock_get(TEST_TRANSACTION_PATH_CSV).return_value = 650703.0

        assert reading_csv_xlsx_file(TEST_TRANSACTION_PATH_CSV)[0]["id"] == 650703.0
        mock_get.assert_called_once_with(TEST_TRANSACTION_PATH_CSV)


def test_reading_file_invalid():
    with patch("src.utils.reading_csv_xlsx_file") as mock_get:
        mock_get(USER_SETTINGS_JSON).return_value = "Неверное расширение файла, задан неправильный путь"

        assert reading_csv_xlsx_file(USER_SETTINGS_JSON) == "Неверное расширение файла, задан неправильный путь"
        mock_get.assert_called_once_with(USER_SETTINGS_JSON)


FAKE_morning = datetime.datetime.strptime("2021-12-30 06:11:12", "%Y-%m-%d %H:%M:%S")
FAKE_afternoon = datetime.datetime.strptime("2021-12-30 13:11:12", "%Y-%m-%d %H:%M:%S")
FAKE_evening = datetime.datetime.strptime("2021-12-30 19:11:12", "%Y-%m-%d %H:%M:%S")
FAKE_night = datetime.datetime.strptime("2021-12-30 01:11:12", "%Y-%m-%d %H:%M:%S")


@pytest.fixture()
def expected_list_dict_json():
    return "<class 'list'>"


@pytest.mark.parametrize("path_json", [TEST_READING_JSON, TEST_UTILS_FileNotFoundError, TEST_UTILS_JSONDecodeError])
def test_get_list_dict_json(path_json, expected_list_dict_json):
    assert f"{type(get_list_dict_json(path_json))}" == expected_list_dict_json


@pytest.fixture
def patch_datetime_morning(monkeypatch):
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = FAKE_morning
    monkeypatch.setattr(datetime, "datetime", datetime_mock)


@pytest.fixture
def patch_datetime_afternoon(monkeypatch):
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = FAKE_afternoon
    monkeypatch.setattr(datetime, "datetime", datetime_mock)


@pytest.fixture
def patch_datetime_evening(monkeypatch):
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = FAKE_evening
    monkeypatch.setattr(datetime, "datetime", datetime_mock)


@pytest.fixture
def patch_datetime_night(monkeypatch):
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = FAKE_night
    monkeypatch.setattr(datetime, "datetime", datetime_mock)


def test_get_greeting_morning(patch_datetime_morning):
    assert get_greeting() == "Доброго утра"


def test_get_greeting_afternoon(patch_datetime_afternoon):
    assert get_greeting() == "Доброго дня"


def test_get_greeting_evening(patch_datetime_evening):
    assert get_greeting() == "Доброго вечера"


def test_get_greeting_night(patch_datetime_night):
    assert get_greeting() == "Доброй ночи"


@pytest.fixture
def str_datetime():
    str_datetime_ = ["2021-12-30 06:11:12", "2021-12-30 06:11"]
    return str_datetime_


def test_get_information_on_card(str_datetime):
    assert get_information_on_card(str_datetime[0]) == [
        {"cashback": 37.76, "last_digits": "*4556", "total_spent": 3775.7},
        {"cashback": 146.22, "last_digits": "*5091", "total_spent": 14622.26},
        {"cashback": 238.05, "last_digits": "*7197", "total_spent": 23805.25},
    ]
    with pytest.raises(ValueError):
        get_information_on_card(str_datetime[1])


def test_get_top5_transactions(str_datetime):
    assert get_top5_transactions(str_datetime[0]) == [
        {"amount": 20000.0, "category": "Другое", "date": "2021-12-23 16:45:12", "description": "Иван С."},
        {
            "amount": 3500.0,
            "category": "Пополнения",
            "date": "2021-12-05 15:20:00",
            "description": "Внесение наличных через банкомат Тинькофф",
        },
        {"amount": -15.0, "category": "Косметика", "date": "2021-12-09 16:03:32", "description": "Улыбка радуги"},
        {"amount": -100.0, "category": "Переводы", "date": "2021-12-09 01:07:48", "description": "Перевод на карту"},
        {"amount": -837.9, "category": "Ж/д билеты", "date": "2021-12-07 14:02:27", "description": "РЖД"},
        {"amount": 1721.38, "category": "Каршеринг", "date": "2021-12-12 15:03:30", "description": "Ситидрайв"},
        {
            "amount": 495.0,
            "category": "Бонусы",
            "date": "2021-12-20 19:35:26",
            "description": "Выплата по вашему обращению",
        },
        {
            "amount": 232.96,
            "category": "Бонусы",
            "date": "2021-12-20 19:40:28",
            "description": "Выплата по вашему обращению",
        },
        {"amount": -1.0, "category": "Каршеринг", "date": "2021-12-17 23:40:14", "description": "Ситидрайв"},
        {"amount": -1.07, "category": "Каршеринг", "date": "2021-12-01 23:40:34", "description": "Ситидрайв"},
        {"amount": 421.0, "category": "Различные товары", "date": "2021-12-20 19:42:13", "description": "Ozon.ru"},
        {"amount": 180.77, "category": "Каршеринг", "date": "2021-12-03 19:05:50", "description": "Ситидрайв"},
        {"amount": 15.0, "category": "Другое", "date": "2021-12-21 22:57:26", "description": "Google"},
        {"amount": -5.7, "category": "Каршеринг", "date": "2021-12-25 15:30:02", "description": "Ситидрайв"},
        {"amount": -7.94, "category": "Каршеринг", "date": "2021-12-21 17:21:58", "description": "Ситидрайв"},
    ]
    with pytest.raises(ValueError):
        get_top5_transactions(str_datetime[1])


@pytest.fixture
def user_settings_stock():
    user_setting = get_list_dict_json(TEST_USER_SETTINGS_JSON)
    user_stocks = user_setting.get("user_stocks")
    return user_stocks


def test_get_user_stocks(user_settings_stock):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "open": 194.45,
            "high": 194.76,
            "low": 192.12,
            "close": 192.32,
            "volume": 39500106.0,
            "adj_high": 194.76,
            "adj_low": 192.11,
            "adj_close": 192.32,
            "adj_open": 194.45,
            "adj_volume": 40895115.0,
            "split_factor": 1.0,
            "dividend": 0.0,
            "symbol": "AAPL",
            "exchange": "XNAS",
            "date": "2023-12-06T00:00:00+0000",
        }
        assert get_user_stocks(user_settings_stock) == [{"price": 192.32, "stock": "AAPL"}]
        mock_get.assert_called_with(
            "http://api.marketstack.com/v1/tickers/AAPL/eod/latest",
            params={"access_key": "865979e56d3f300f7c1184eb37d2898e"},
        )


@patch("requests.get")
def test_get_user_stocks_invalid(mock_get, user_settings_stock):
    exception = HTTPError(mock.Mock(status=404), "not found")
    mock_get(mock.ANY).raise_for_status.side_effect = exception

    with pytest.raises(SystemExit) as error_info:
        get_user_stocks(user_settings_stock)
        assert error_info == exception


@pytest.fixture
def user_settings_currencies():
    user_setting = get_list_dict_json(TEST_USER_SETTINGS_JSON)
    user_currencies = user_setting.get("user_currencies")
    return user_currencies


@patch("requests.get")
def test_get_user_currencies(mock_get, user_settings_currencies):
    mock_get.return_value.json.return_value = {
        "base": "USD",
        "date": "2023-12-07",
        "rates": {"RUB": 92.42499},
        "success": True,
        "timestamp": 1701981182,
    }

    assert get_user_currencies(user_settings_currencies) == [{"currency": "USD", "rate": 92.42499}]
    mock_get.assert_called_with(
        "https://api.apilayer.com/fixer/latest?symbols=RUB&base=USD",
        headers={"apikey": "cKV92Nc3qbTXs6Dr0VzUlBc7s6EulHJH"},
    )


@patch("requests.get")
def test_get_user_currencies_invalid(mock_get, user_settings_currencies):
    exception = HTTPError(mock.Mock(status=404), "not found")
    mock_get(mock.ANY).raise_for_status.side_effect = exception

    with pytest.raises(SystemExit) as error_info:
        get_user_currencies(user_settings_currencies)
        assert error_info == exception
