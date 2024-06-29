import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd

from src.reports import calculate_expenses, find_transactions


class TestFinancialAnalysis(unittest.TestCase):

    @patch("pandas.read_excel")
    def test_find_transactions(self, mock_read_excel: MagicMock) -> None:
        # Подготовка тестовых данных
        mock_read_excel.return_value = pd.DataFrame(
            {
                "Описание": ["Перевод", "Оплата услуг", "Перевод"],
                "Категория": ["Переводы", "Услуги", "Переводы"],
                "Сумма платежа": [1000, 2000, 1500],
            }
        )

        # Вызов функции для тестирования
        result = find_transactions("Перевод")
        # Проверка результата
        self.assertIn("Перевод", result)

    @patch("pandas.read_excel")
    def test_calculate_expenses(self, mock_read_excel: MagicMock) -> None:
        # Подготовка тестовых данных
        mock_read_excel.return_value = pd.DataFrame(
            {
                "Категория": ["Переводы", "Услуги", "Переводы"],
                "Дата платежа": ["01.01.2024", "01.02.2024", "01.03.2024"],
                "Сумма платежа": [1000, 2000, 1500],
            }
        )
        mock_read_excel.return_value["Дата платежа"] = pd.to_datetime(
            mock_read_excel.return_value["Дата платежа"], format="%d.%m.%Y"
        )

        # Вызов функции для тестирования
        result = calculate_expenses(mock_read_excel.return_value,
                                    "Переводы", datetime(2024, 3, 1))
        # Проверка результата
        self.assertIn("Переводы", result)
        self.assertIn("Общие расходы", result)


if __name__ == "__main__":
    unittest.main()
