from unittest.mock import patch

from src.views import get_json_data


@patch("src.views.get_information_on_card")
@patch("src.views.get_top5_transactions")
@patch("src.views.get_list_dict_json")
@patch("src.views.get_user_stocks")
@patch("src.views.get_user_currencies")
@patch("src.views.get_greeting")
def test_get_json_data(
    mock_get_greeting,
    mock_get_user_currencies,
    mock_get_user_stocks,
    mock_get_list_dict_json,
    mock_get_top5_transactions,
    mock_get_information_on_card,
):
    mock_get_greeting.return_value = "Доброго утра"
    mock_get_information_on_card.return_value = [
        {"cashback": 37.76, "last_digits": "*4556", "total_spent": 3775.7},
        {"cashback": 146.22, "last_digits": "*5091", "total_spent": 14622.26},
        {"cashback": 238.05, "last_digits": "*7197", "total_spent": 23805.25},
    ]
    mock_get_top5_transactions.return_value = [
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
    mock_get_list_dict_json.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mock_get_user_stocks.return_value = [{"price": 192.32, "stock": "AAPL"}]
    mock_get_user_currencies.return_value = [{"currency": "USD", "rate": 92.42499}]
    assert get_json_data("2021-12-30 06:11:12") == (
        '{"greeting": "Доброго утра", "cards": [{"cashback": 37.76, "last_digits": '
        '"*4556", "total_spent": 3775.7}, {"cashback": 146.22, "last_digits": '
        '"*5091", "total_spent": 14622.26}, {"cashback": 238.05, "last_digits": '
        '"*7197", "total_spent": 23805.25}], "top_transactions": [{"amount": 20000.0, '
        '"category": "Другое", "date": "2021-12-23 16:45:12", "description": "Иван '
        'С."}, {"amount": 3500.0, "category": "Пополнения", "date": "2021-12-05 '
        '15:20:00", "description": "Внесение наличных через банкомат Тинькофф"}, '
        '{"amount": -15.0, "category": "Косметика", "date": "2021-12-09 16:03:32", '
        '"description": "Улыбка радуги"}, {"amount": -100.0, "category": "Переводы", '
        '"date": "2021-12-09 01:07:48", "description": "Перевод на карту"}, '
        '{"amount": -837.9, "category": "Ж/д билеты", "date": "2021-12-07 14:02:27", '
        '"description": "РЖД"}, {"amount": 1721.38, "category": "Каршеринг", "date": '
        '"2021-12-12 15:03:30", "description": "Ситидрайв"}, {"amount": 495.0, '
        '"category": "Бонусы", "date": "2021-12-20 19:35:26", "description": "Выплата '
        'по вашему обращению"}, {"amount": 232.96, "category": "Бонусы", "date": '
        '"2021-12-20 19:40:28", "description": "Выплата по вашему обращению"}, '
        '{"amount": -1.0, "category": "Каршеринг", "date": "2021-12-17 23:40:14", '
        '"description": "Ситидрайв"}, {"amount": -1.07, "category": "Каршеринг", '
        '"date": "2021-12-01 23:40:34", "description": "Ситидрайв"}, {"amount": '
        '421.0, "category": "Различные товары", "date": "2021-12-20 19:42:13", '
        '"description": "Ozon.ru"}, {"amount": 180.77, "category": "Каршеринг", '
        '"date": "2021-12-03 19:05:50", "description": "Ситидрайв"}, {"amount": 15.0, '
        '"category": "Другое", "date": "2021-12-21 22:57:26", "description": '
        '"Google"}, {"amount": -5.7, "category": "Каршеринг", "date": "2021-12-25 '
        '15:30:02", "description": "Ситидрайв"}, {"amount": -7.94, "category": '
        '"Каршеринг", "date": "2021-12-21 17:21:58", "description": "Ситидрайв"}], '
        '"currency_rates": [{"currency": "USD", "rate": 92.42499}], "stock_prices": '
        '[{"price": 192.32, "stock": "AAPL"}]}'
    )
