import datetime
import json
import logging
import re
from os import PathLike
from typing import Any

import numpy as np
import pandas as pd
import requests

from data.config import OPERATIONS_XLS, LOG_VIEWS_PATH, LOG_UTILS_PATH


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
        logging_utils().error("Неверное расширение файла, задан неправильный путь")
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
        logging_utils().error("Файл JSON не найден")
        file_json = []

    except json.JSONDecodeError:
        logging_utils().error("Файл не содержит JSON формат")
        file_json = []

    return file_json


def get_greeting() -> str:
    """Функция выдает приветствие в зависимости от времени суток
    :return: Доброго дня/ночи/утра/вечера - greeting"""
    date_obj = datetime.datetime.now()
    greeting = "Доброго дня"
    if 0 <= date_obj.hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= date_obj.hour < 12:
        greeting = "Доброго утра"
    elif 18 <= date_obj.hour:
        greeting = "Доброго вечера"
    return greeting


def get_information_on_card(str_datetime: str) -> Any:
    """Функция принимает строку формата 'YYYY-MM-DD HH:MM:SS'
    возращает информацию в виде списка словарей за промежуток времени с начала месяца указанной в строке str_datetime
    По каждой карте:
    - Последние 4 цифры карты
    - Общая сумма расходов
    - Кэшбэк (1 рубль на каждые 100 рублей)
    :param str_datetime
    :return expenses_list_dict"""

    try:
        date_obj = datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
        file_xls = reading_csv_xlsx_file(OPERATIONS_XLS)
        df = pd.DataFrame(file_xls)

        start_date = date_obj.date().replace(day=1)
        end_date = date_obj.date()

        df["Сумма платежа"] = df["Сумма платежа"].apply(lambda x: x if x < 0 else 0)
        df["Дата операции"] = df["Дата операции"].apply(lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M:%S"))

        df.rename(columns={"Дата операции": "date"}, inplace=True)
        df = df.loc[(df.date >= np.datetime64(start_date)) & (df.date <= np.datetime64(end_date))]

        expenses = df.groupby("Номер карты")["Сумма платежа"].sum().reset_index()
        expenses.rename(
            columns={"Номер карты": "last_digits", "Сумма платежа": "total_spent"},
            inplace=True,
        )
        expenses = expenses.assign(cashback=round(expenses.total_spent * 0.01, 2))
        expenses.update(expenses.select_dtypes(include=[np.number]).abs())
        expenses_list_dict = expenses.to_dict(orient="records")
        for expense in expenses_list_dict:
            expense["total_spent"] = round(expense.get("total_spent"), 2)
        return expenses_list_dict
    except ValueError:

        logging_utils().error("Формат str_datetime неккоректен")
        raise ValueError("Формат строки неккоректен")


def get_top5_transactions(str_datetime: str) -> Any:
    """Функция принимает строку формата 'YYYY-MM-DD HH:MM:SS'
    возращает информацию в виде списка словарей за промежуток времени с начала месяца указанной в строке str_datetime
    топ 5 транзакций по каждой карте
    :param str_datetime
    :return top_5_list_dict"""

    try:
        date_obj = datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
        file_xls = reading_csv_xlsx_file(OPERATIONS_XLS)
        df = pd.DataFrame(file_xls)

        start_date = date_obj.date().replace(day=1)
        end_date = date_obj.date()

        df["Дата операции"] = df["Дата операции"].apply(lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M:%S"))

        df.rename(columns={"Дата операции": "date"}, inplace=True)
        df = df.loc[(df.date >= np.datetime64(start_date)) & (df.date <= np.datetime64(end_date))]

        cards = df.groupby("Номер карты")
        top_5 = cards.apply(lambda x: x.sort_values("Сумма платежа", ascending=False).head(5))
        top_5.rename(
            columns={
                "Сумма платежа": "amount",
                "Категория": "category",
                "Описание": "description",
                "Дата операции": "date",
            },
            inplace=True,
        )
        top_5 = top_5.iloc[:, [0, 6, 9, 11]]

        top_5_list_dict = top_5.to_dict(orient="records")
        for top_5 in top_5_list_dict:
            top_5["date"] = str(top_5.get("date"))
        return top_5_list_dict

    except ValueError:

        logging_utils().error("Формат str_datetime неккоректен")
        raise ValueError("Формат строки неккоректен")


def get_user_stocks(user_stocks: list) -> list[dict]:
    """Функция принимает на вход список акций и возвращает список словарей c символом акции и ценой
    :param user_stocks
    :return data_user_stocks"""
    data_user_stocks = []
    for user_stock in user_stocks:
        url = "http://api.marketstack.com/v1/tickers/STOCK/eod/latest"
        url = re.sub("STOCK", user_stock, url, count=0, flags=re.IGNORECASE)
        try:
            params = {"access_key": "865979e56d3f300f7c1184eb37d2898e"}
            response = requests.get(url, params=params)
            api_response = response.json()
            response.raise_for_status()
            data_user_stocks.append(
                {
                    "stock": api_response.get("symbol"),
                    "price": api_response.get("adj_close"),
                }
            )
        except requests.exceptions.HTTPError as err:
            logging_utils().error(f"Ошибка запроса requests.get -> {err}")

            raise SystemExit(err)

    return data_user_stocks


def get_user_currencies(user_currencies: list) -> list[dict]:
    """Функция принимает на вход список валют и возвращает список словарей c символом валют и ценой к рублю
    :param user_currencies
    :return data_user_currencies"""
    data_user_currencies = []
    for user_currency in user_currencies:
        url = "https://api.apilayer.com/fixer/latest?symbols=RUB&base=CURRENCY"
        url = re.sub("CURRENCY", user_currency, url, count=0, flags=re.IGNORECASE)

        headers = {"apikey": "cKV92Nc3qbTXs6Dr0VzUlBc7s6EulHJH"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            data_user_currencies.append(
                {
                    "currency": result.get("base"),
                    "rate": (result.get("rates")).get("RUB"),
                }
            )
        except requests.exceptions.HTTPError as err:
            logging_utils().error(f"Ошибка запроса requests.get -> {err}")
            raise SystemExit(err)
    return data_user_currencies


def logging_utils() -> Any:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s -%(funcName)s -%(lineno)d\n",
        filename=LOG_UTILS_PATH,
        filemode="a",
        encoding="utf-8",
    )

    return logging.getLogger()


def logging_views() -> Any:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s -%(funcName)s -%(lineno)d\n",
        filename=LOG_VIEWS_PATH,
        filemode="a",
        encoding="utf-8",
    )

    return logging.getLogger()
