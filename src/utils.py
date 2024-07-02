import json
from typing import Any

import pandas as pd


def load_xlsx_data(xlsx_path: str) -> Any:
    """Загружает данные из Excel файла."""
    data_frame = pd.read_excel(xlsx_path)
    return data_frame.to_dict("records")


def save_to_json(data: dict, file_path: str) -> None:
    """Сохраняет данные в JSON-файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
