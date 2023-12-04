import datetime
import json
import re
from os import PathLike
from typing import Any

import numpy as np
import pandas as pd
import requests

from data.config import OPERATIONS_XLS


def reading_csv_xlsx_file(path: PathLike) -> Any:
    """Функция считывание финансовых операций с CSV- и XLSX-файлов
    param path: путь к файлу
    return: список словарей с данными
    """
    path_str = str(path)

    if path_str.endswith(".csv"):
        results = pd.read_csv(path, sep=";")

    elif path_str.endswith(".xlsx"):
        results = pd.read_excel(path)

    elif path_str.endswith(".xls"):
        results = pd.read_excel(path)

    else:
        return "Неверное расширение файла, задан неправильный путь"

    results = pd.DataFrame(results).replace({np.nan: None})
    result_list_dict = results.to_dict(orient="records")

    return result_list_dict


def get_list_dict_json(path_json: PathLike) -> Any:
    """Принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях
    :param path_json: путь до JSON-файла
    :return file_json список словарей с данными о финансовых транзакциях
    (Если файл пустой, содержит не список или не найден, функция возвращает пустой список)
    """
    # logger_utils = logging_utils()
    try:
        with open(path_json, encoding="utf-8") as file:
            file_json = json.load(file)
            # logger_utils.info("Файл JSON-файла успешно загружен")

    except FileNotFoundError:
        # logger_utils.error("Файл JSON не найден")
        file_json = []

    except json.JSONDecodeError:
        # logger_utils.error("Файл не содержит JSON формат")
        file_json = []

    return file_json


def get_greeting() -> str:
    date_obj = datetime.datetime.now()
    greeting = 'Доброго дня'
    if 0 <= date_obj.hour < 6:
        greeting = 'Доброй ночи'
    elif 6 <= date_obj.hour < 12:
        greeting = 'Доброго утра'
    elif 18 <= date_obj.hour:
        greeting = 'Доброго вечера'
    return greeting


def get_information_on_card(str_datetime: str) -> Any:
    date_obj = datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    file_xls = reading_csv_xlsx_file(OPERATIONS_XLS)
    df = pd.DataFrame(file_xls)

    start_date = date_obj.date().replace(day=1)
    end_date = date_obj.date()

    df['Сумма платежа'] = df['Сумма платежа'].apply(lambda x: x if x < 0 else 0)
    df['Дата операции'] = df['Дата операции'].apply(
        lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M:%S"))

    df.rename(columns={'Дата операции': 'date'}, inplace=True)
    df = df.loc[(df.date >= np.datetime64(start_date)) & (df.date <= np.datetime64(end_date))]

    expenses = df.groupby('Номер карты')['Сумма платежа'].sum().reset_index()
    expenses.rename(columns={'Номер карты': 'last_digits', 'Сумма платежа': 'total_spent'}, inplace=True)
    expenses = expenses.assign(cashback=round(expenses.total_spent * 0.01, 2))
    expenses.update(expenses.select_dtypes(include=[np.number]).abs())
    expenses_list_dict = expenses.to_dict(orient="records")
    for expense in expenses_list_dict:
        expense['total_spent'] = round(expense.get('total_spent'), 2)
    return expenses_list_dict


def get_top5_transactions(str_datetime: str) -> Any:
    date_obj = datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    file_xls = reading_csv_xlsx_file(OPERATIONS_XLS)
    df = pd.DataFrame(file_xls)

    start_date = date_obj.date().replace(day=1)
    end_date = date_obj.date()

    df['Дата операции'] = df['Дата операции'].apply(
        lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M:%S"))

    df.rename(columns={'Дата операции': 'date'}, inplace=True)
    df = df.loc[(df.date >= np.datetime64(start_date)) & (df.date <= np.datetime64(end_date))]

    cards = df.groupby('Номер карты')
    top_5 = cards.apply(lambda x: x.sort_values('Сумма платежа', ascending=False).head(5))
    top_5.rename(columns={'Сумма платежа': 'amount', 'Категория': 'category', 'Описание': 'description',
                          'Дата операции': 'date'}, inplace=True)
    top_5 = top_5.iloc[:, [0, 6, 9, 11]]

    top_5_list_dict = top_5.to_dict(orient="records")
    for top_5 in top_5_list_dict:
        top_5['date'] = str(top_5.get('date'))
    return top_5_list_dict


def get_user_stocks(user_stocks: list) -> Any:
    data_user_stocks = []
    for user_stock in user_stocks:
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=STOCKS&apikey=KC8AK2RF3WYT76C2'
        url = re.sub('STOCK', user_stock, url, count=0, flags=re.IGNORECASE)
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            data_user_stocks.append(result)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    return data_user_stocks


def get_user_currencies(user_currencies: list) -> Any:
    data_user_currencies = []
    for user_currency in user_currencies:
        url = "https://api.apilayer.com/fixer/latest?symbols=RUB&base=CURRENCY"
        url = re.sub('CURRENCY', user_currency, url, count=0, flags=re.IGNORECASE)

        headers = {
            "apikey": "cKV92Nc3qbTXs6Dr0VzUlBc7s6EulHJH"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            data_user_currencies.append(result)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    return data_user_currencies
