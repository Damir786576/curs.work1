import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv

from src.utils import load_xlsx_data, save_to_json

# Настройка логирования
logging.basicConfig(filename="views.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

# Ключ для доступа к API
SECRET_KEY = os.getenv("API_KEY")
SECRET_LINK = os.getenv("API_LINK")


def welcome_message(time_str: str | None) -> str:
    logging.info("Функция welcome_message вызвана")
    """Возвращает приветственное сообщение в зависимости от времени суток."""
    try:
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
    except Exception as e:
        logging.error(f"Ошибка в функции welcome_message: {e}")
        raise


def sum_expenses(df: pd.DataFrame) -> Any:
    logging.info("Функция sum_expenses вызвана")
    """Считает сумму расходов из DataFrame операций."""
    try:
        expenses = df[df["Сумма операции"] < 0]["Сумма операции"].abs().sum()
        return expenses
    except Exception as e:
        logging.error(f"Ошибка в функции sum_expenses: {e}")
        raise


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
    sorted_transactions = sorted(trans_list, key=lambda x: x.get("transaction_amount", 0), reverse=True)[:5]
    top_transactions = []
    for transaction in sorted_transactions[:5]:
        top_transaction = {
            "date": transaction["Дата операции"].split(" ")[0],
            "amount": abs(transaction["Сумма операции"]),
            "category": transaction["Категория"],
            "description": transaction["Описание"],
        }
        top_transactions.append(top_transaction)

    return top_transactions


def fetch_currency_value(curr: str) -> Optional[float]:
    """Получает курс валюты к рублю."""
    endpoint = f"{SECRET_LINK}/{curr}"
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


def main_views() -> None:
    logging.info("Функция main_views вызвана")
    try:
        greeting = welcome_message(None)
        print(greeting)
        transactions_list = load_xlsx_data("../data/operations.xls")

        # Создаем DataFrame из списка транзакций
        transactions_df = pd.DataFrame(transactions_list)

        # Анализ расходов
        total_expenses = sum_expenses(transactions_df)
        print(f"Общая сумма расходов: {total_expenses}")

        # Анализ использования карт
        card_usage = analyze_card_usage(transactions_list)
        print(f"Информация об использовании карт: {card_usage}")

        # Получение крупнейших операций в новом формате
        largest_ops = largest_transactions(transactions_list)
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
        output_file = "operations_views.json"
        save_to_json(output_data, output_file)

        print(f"Данные успешно сохранены в файл {output_file}")
    except Exception as e:
        logging.error(f"Ошибка в функции main_views: {e}")
        raise


if __name__ == "__main__":
    main_views()
