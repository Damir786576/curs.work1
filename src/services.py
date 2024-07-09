import json
import logging
import re
from typing import Dict, List

import pandas as pd

# Настройка логирования
logging.basicConfig(filename="services.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


def read_transactions_xls(file_path: str) -> List[Dict]:
    """Читает финансовые транзакции из XLSX файла."""
    try:
        data_frame = pd.read_excel(file_path)
        transactions = data_frame.to_dict(orient="records")
        logging.info("Транзакции успешно прочитаны из файла.")
        return transactions
    except Exception as e:
        logging.error(f"Ошибка при чтении файла: {e}")
        raise


def search_by_description(transactions: List[Dict], query: str) -> List[Dict]:
    """Ищет транзакции, соответствующие данному описанию запроса."""
    if query == "":
        return []
    try:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        matching_transactions = [
            transaction for transaction in transactions if pattern.search(transaction["Описание"])
        ]
        logging.info(f"Найдено {len(matching_transactions)} транзакций по запросу: '{query}'.")
        return matching_transactions
    except Exception as e:
        logging.error(f"Ошибка при поиске транзакций: {e}")
        raise


def write_to_json(file_path: str, data: List[Dict]) -> None:
    """Записывает данные в JSON файл и выводит их в консоль."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Данные успешно записаны в файл {file_path}.")
        print(json.dumps(data, ensure_ascii=False, indent=4))
    except Exception as e:
        logging.error(f"Ошибка при записи в файл: {e}")
        raise


def main_services() -> None:
    """Основная функция для выполнения скрипта."""
    try:
        file_path = "../data/operations.xls"
        json_output_path = "../src/matching_services.json"
        query = input("Введите поисковый запрос: ")

        transactions = read_transactions_xls(file_path)
        matching_services = search_by_description(transactions, query)

        # Запись результатов в JSON файл
        write_to_json(json_output_path, matching_services)

        print(f"Результаты поиска были записаны в файл: {json_output_path}")
    except Exception as e:
        logging.error(f"Ошибка в функции main_services: {e}")
        raise


if __name__ == "__main__":
    main_services()
