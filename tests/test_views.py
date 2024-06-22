import unittest
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.views import (analyze_card_usage, fetch_currency_value, get_stock_currency, load_xlsx_data, run_application,
                       save_to_json, sum_expenses, welcome_message)


class TestFinancialFunctions(unittest.TestCase):
    def test_welcome_message(self) -> None:
        """Тестирует вывод приветственного сообщения в зависимости от времени суток."""
        morning_time = "2024-06-22 09:00:00"
        self.assertEqual(welcome_message(morning_time), "Доброе утро!")
        # Добавьте тесты для других времен суток

    def test_sum_expenses(self) -> None:
        """Тестирует подсчет суммы расходов из списка транзакций."""
        transactions = [{"Сумма операции": -100}, {"Сумма операции": 200}, {"Сумма операции": -50}]
        self.assertEqual(sum_expenses(transactions), 150)
        # Добавьте тесты с разными данными

    @patch("pandas.read_excel")
    def test_load_xlsx_data(self, mock_read_excel: Any) -> None:
        """Мокирует функцию pandas.read_excel и тестирует загрузку данных из xlsx файла."""
        mock_read_excel.return_value.to_dict.return_value = "mocked_data"
        self.assertEqual(load_xlsx_data("fake_path"), "mocked_data")

    def test_analyze_card_usage(self) -> None:
        """Тестирует анализ использования карты по списку операций."""
        ops = [
            {"Номер карты": 1234567890123456, "Сумма операции": -100, "Бонусы (включая кэшбэк)": 10},
            # Добавьте другие операции для тестирования
        ]
        expected_result = [{"end_digits": "23456", "spent": 100.0, "bonus": 10.0}]
        self.assertEqual(analyze_card_usage(ops), expected_result)

    @patch("requests.get")
    def test_fetch_currency_value(self, mock_get: Any) -> None:
        """Мокирует запросы к API и тестирует получение курса валюты."""
        mock_response = {"conversion_rates": {"RUB": 75.0}}
        mock_get.return_value.json.return_value = mock_response
        self.assertEqual(fetch_currency_value("USD"), 75.0)

    @patch("yfinance.Ticker")
    def test_get_stock_currency(self, mock_yfinance: Any) -> None:
        """Мокирует yfinance и тестирует получение текущей цены акции."""
        mock_yfinance.return_value.history.return_value = pd.DataFrame({"Close": [100.0]})
        self.assertEqual(get_stock_currency("AAPL"), 100.0)

    @patch("json.dump")
    def test_save_to_json(self, mock_json_dump: Any) -> None:
        """Тестирует сохранение данных в JSON-файл."""
        save_to_json({"test": "data"}, "fake_path")
        mock_json_dump.assert_called_once()

    @patch("builtins.print")
    def test_run_application(self, mock_print: Any) -> None:
        """Тестирует основную функцию приложения."""
        with patch("src.views.load_xlsx_data", return_value=[]), patch(
            "src.views.fetch_currency_value", return_value=75.0
        ), patch("src.views.get_stock_currency", return_value=100.0):
            run_application()
            mock_print.assert_called()


if __name__ == "__main__":
    unittest.main()
