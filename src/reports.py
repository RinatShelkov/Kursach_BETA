import datetime
import pprint
from os import PathLike
from typing import Optional

import numpy as np
import pandas as pd

from data.config import TEST_OPERATIONS_XLS
from src.utils import reading_csv_xlsx_file


def spending_by_category(transactions: PathLike, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция принимает на вход:
    :param transactions - датафрейм с транзакциями
    :param category - название категории
    :param date - опциональную дату
    Если дата не передана, то берется текущая дата.
    :return pd.DataFrame
    Функция возвращает траты по заданной категории
    за последние 3 месяца (от переданной даты, формат даты 'YYYY-MM-DD HH:MM:SS').
    Если по данной категории не найдена информация  вернется пустой датафрейм"""

    if date is None:
        date_search = datetime.datetime.now()
    else:
        date_search = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    result = []
    file_ = reading_csv_xlsx_file(transactions)

    df = pd.DataFrame(file_)

    start_date = date_search.date().replace(month=(date_search.date().month - 3))
    end_date = date_search.date()

    df["Дата операции"] = df["Дата операции"].apply(lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M:%S"))

    df.rename(columns={"Дата операции": "date"}, inplace=True)
    df = df.loc[(df.date >= np.datetime64(start_date)) & (df.date <= np.datetime64(end_date))]

    df = df.to_dict(orient="records")
    for row in df:
        if row["Категория"] == category:
            result.append(row)
    result = pd.DataFrame(result)

    return result


pprint.pprint(spending_by_category(TEST_OPERATIONS_XLS, "Супермаркеты", "2021-12-30 06:11:12"))
