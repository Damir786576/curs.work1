import json
import re
from typing import Dict, List

import pandas as pd


def read_transactions_xls(file_path: str) -> List[Dict]:
    """Читает финансовые транзакции из XLSX файла."""
    data_frame = pd.read_excel(file_path)
    transactions = data_frame.to_dict(orient="records")
    return transactions


def search_by_description(transactions: List[Dict], query: str) -> List[Dict]:
    """Ищет транзакции, соответствующие данному описанию запроса."""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction["Описание"])]


def write_to_json(file_path: str, data: List[Dict]) -> None:
    """Записывает данные в JSON файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main() -> None:
    """Основная функция для выполнения скрипта."""
    file_path = "../data/operations.xls"
    json_output_path = "../src/matching_transactions.json"
    query = input("Введите поисковый запрос: ")

    transactions = read_transactions_xls(file_path)
    matching_transactions = search_by_description(transactions, query)

    # Запись результатов в JSON файл
    write_to_json(json_output_path, matching_transactions)

    print(f"Результаты поиска были записаны в файл: {json_output_path}")


if __name__ == "__main__":
    main()
