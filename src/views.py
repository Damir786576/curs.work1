import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

# Ключ для доступа к API
SECRET_KEY = os.getenv("2a2bb6d5daa5c58f8871e1e8")


def welcome_message(time_str: str | None) -> str:
    """Возвращает приветственное сообщение в зависимости от времени суток."""
    current_time = datetime.now() if time_str is None else datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 23:
        return "Добрый вечер!"
    else:
        return "Спокойной ночи!"


def sum_expenses(trans_list: List[Dict[str, Any]]) -> float:
    """Считает сумму расходов из списка операций."""
    expenses = 0
    for transaction in trans_list:
        if "Сумма операции" in transaction and transaction["Сумма операции"] < 0:
            expenses += abs(transaction["Сумма операции"])
    return expenses


def load_xlsx_data(xlsx_path: str) -> Any:
    """Загружает данные из Excel файла."""
    data_frame = pd.read_excel(xlsx_path)
    return data_frame.to_dict("records")


def analyze_card_usage(ops: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Анализирует использование карт по операциям."""
    usage_info = {}
    for op in ops:
        card_number = op.get("Номер карты")
        if card_number is not None:
            card_number_str = str(card_number)
            card_end = card_number_str[-5:]
            if card_end not in usage_info:
                usage_info[card_end] = {"end_digits": card_end, "spent": 0.0, "bonus": 0.0}
            transaction_amount = op.get("Сумма операции", 0)
            bonuses_including_cashback = op.get("Бонусы (включая кэшбэк)", 0.0)
            if transaction_amount < 0:
                usage_info[card_end]["spent"] += abs(transaction_amount)
            usage_info[card_end]["bonus"] += bonuses_including_cashback
        else:
            print("Внимание: Операция без номера карты:", op)
    return list(usage_info.values())


def largest_transactions(trans_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Возвращает пять самых крупных транзакций."""

    for transaction in trans_list:
        transaction["Кэшбэк"] = transaction.get("Кэшбэк", 0)

    return sorted(trans_list, key=lambda x: x.get("transaction_amount", 0), reverse=True)[:5]


def fetch_currency_value(curr: str) -> Optional[float]:
    """Получает курс валюты к рублю."""
    endpoint = f"https://v6.exchangerate-api.com/v6/2a2bb6d5daa5c58f8871e1e8/latest/{curr}"
    result = requests.get(endpoint)
    result.raise_for_status()
    data = result.json()
    rub_value = data["conversion_rates"].get("RUB")
    return rub_value if rub_value else None


def get_stock_currency(ticker: str) -> float:
    """Получает текущую цену акции."""
    stock_info = yf.Ticker(ticker)
    today_info = stock_info.history(period="1d")
    return float(today_info["Close"].iloc[-1])


def execute_main() -> None:
    """Основная функция, выполняющая анализ данных."""
    time_input = input("Введите время (YYYY-MM-DD HH:MM:SS) или Enter для текущего: ")
    message = welcome_message(time_input or None)
    print(message)


def save_to_json(data: dict, file_path: str) -> None:
    """Сохраняет данные в JSON-файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def run_application() -> None:
    greeting = welcome_message(None)
    print(greeting)
    transactions = load_xlsx_data("C:\\Users\\Zver\\Desktop\\pythonProject7\\data\\operations.xls")

    # Анализ расходов
    total_expenses = sum_expenses(transactions)
    print(f"Общая сумма расходов: {total_expenses}")

    # Анализ использования карт
    card_usage = analyze_card_usage(transactions)
    print(f"Информация об использовании карт: {card_usage}")

    # Получение крупнейших операций
    largest_ops = largest_transactions(transactions)
    print(f"Топ-5 крупнейших операций: {largest_ops}")

    # Получение курса валюты
    usd_value = fetch_currency_value("USD")
    print(f"Курс доллара: {usd_value}")
    eur_value = fetch_currency_value("EUR")
    print(f"Курс евро: {eur_value}")

    # Получение текущей цены акции
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    stock_prices = [{"stock": stock, "price": get_stock_currency(stock)} for stock in stocks]
    print(f"Текущие цены акций: {stock_prices}")

    # Подготовка данных для сохранения
    output_data = {
        "greeting": greeting,
        "total_expenses": total_expenses,
        "card_usage": card_usage,
        "largest_transactions": largest_ops,
        "currency_rates": {"USD": usd_value, "EUR": eur_value},
        "stock_prices": stock_prices,
    }

    # Сохранение данных в JSON-файл
    output_file = "operations_data.json"
    save_to_json(output_data, output_file)


if __name__ == "__main__":
    run_application()
