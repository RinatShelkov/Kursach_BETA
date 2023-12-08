import json
import pprint
from typing import Any

import pandas as pd

from data.config import OPERATIONS_XLS
from src.utils import reading_csv_xlsx_file


def simple_search(str_description_category: str) -> Any:
    """Пользователь передает строку для поиска , возвращается json-ответ со всеми транзакциями,
    содержащими запрос в описании или категории
    :param str_description_category
    :return json_data"""
    file_operation = reading_csv_xlsx_file(OPERATIONS_XLS)
    df = pd.DataFrame(file_operation)
    df = df.to_dict(orient="records")
    result = []
    for row in df:
        if row["Категория"] == str_description_category or row["Описание"] == str_description_category:
            result.append(row)

    json_data = json.dumps(result, ensure_ascii=False)

    return json_data
