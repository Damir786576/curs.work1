import json  # import library JSON for work with it.
from typing import Any  # Import Any for type annotations.

import pandas as pd  # import pandas for data processing and analysis.


# Loads data from an Excel file.
def load_xlsx_data(xlsx_path: str) -> Any:
    data_frame = pd.read_excel(xlsx_path)
    return data_frame.to_dict("records")


# Saves the data to a JSON file.
def save_to_json(data: dict, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
