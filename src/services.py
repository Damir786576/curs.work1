import json  # import library JSON for work with it.
import logging  # import the logging library for logging tasks.
import re  # Import regular expression library for string matching.
from typing import Dict, List  # Import Dict and List for type annotations.

import pandas as pd  # import pandas for data processing and analysis.

# Logging Setup
logging.basicConfig(filename="services.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


# Read financial transactions from an XLSX file.
def read_transactions_xls(file_path: str) -> List[Dict]:
    try:
        data_frame = pd.read_excel(file_path)  # Read the Excel file into a DataFrame.
        transactions = data_frame.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries.
        logging.info("Транзакции успешно прочитаны из файла.")
        return transactions
    except Exception as e:
        logging.error(f"Ошибка при чтении файла: {e}")
        raise


# Searches for transactions matching the given query description.
def search_by_description(transactions: List[Dict], query: str) -> List[Dict]:
    if query == "":
        return []  # Return an empty list if the query is empty.
    try:
        pattern = re.compile(re.escape(query), re.IGNORECASE)  # Ignore the high case
        matching_transactions = [
            transaction for transaction in transactions if pattern.search(transaction["Описание"])
            # Filter transactions.
        ]
        logging.info(f"Найдено {len(matching_transactions)} транзакций по запросу: '{query}'.")
        return matching_transactions
    # write the error if it occurs
    except Exception as e:
        logging.error(f"Ошибка при поиске транзакций: {e}")
        raise


# Writes data to a JSON file and outputs it to the console.
def write_to_json(file_path: str, data: List[Dict]) -> None:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # Write JSON data to file.
        logging.info(f"Данные успешно записаны в файл {file_path}.")
        print(json.dumps(data, ensure_ascii=False, indent=4))  # Print JSON data to console.
        # write the error if it occurs
    except Exception as e:
        logging.error(f"Ошибка при записи в файл: {e}")
        raise


# The basic function to execute a script.
def main_services() -> None:
    try:
        file_path = "../data/operations.xls"  # Path to the input Excel file.
        json_output_path = "../src/matching_services.json"  # Path for the output JSON file.
        query = input("Введите поисковый запрос: ")  # Get user input for the search query.

        transactions = read_transactions_xls(file_path)  # Read transactions from the Excel
        matching_services = search_by_description(transactions, query)  # Search for matching transactions.

        # Write results to JSON file.
        write_to_json(json_output_path, matching_services)

        # Inform the user of the result.
        print(f"Результаты поиска были записаны в файл: {json_output_path}")
    except Exception as e:
        logging.error(f"Ошибка в функции main_services: {e}")
        raise


if __name__ == "__main__":
    main_services()
