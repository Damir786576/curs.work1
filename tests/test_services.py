import unittest
from typing import Any, Dict, List
from unittest.mock import patch

from src.services import read_transactions_xls, search_by_description, write_to_json


class TestFinancialTransactions(unittest.TestCase):

    def setUp(self) -> None:
        """Подготавливает тестовые данные перед каждым тестом."""
        self.sample_transactions: List[Dict[str, Any]] = [
            {"Описание": "Перевод средств", "Сумма": 1000},
            {"Описание": "Оплата услуг", "Сумма": 2000},
            {"Описание": "Перевод средств", "Сумма": 1500},
        ]

    @patch("pandas.read_excel")
    def test_read_transactions_xls(self, mock_read_excel: Any) -> None:
        """Тестирует чтение транзакций из xls файла."""
        mock_read_excel.return_value.to_dict.return_value = self.sample_transactions
        result = read_transactions_xls("dummy_path")
        self.assertEqual(result, self.sample_transactions)

    def test_search_by_description(self) -> None:
        """Тестирует поиск транзакций по описанию."""
        query = "Перевод средств"
        result = search_by_description(self.sample_transactions, query)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(transaction["Описание"] == query for transaction in result))

    @patch("builtins.open")
    @patch("json.dump")
    def test_write_to_json(self, mock_json_dump: Any, mock_open: Any) -> None:
        """Тестирует запись данных в json файл."""
        write_to_json("dummy_path", self.sample_transactions)
        mock_open.assert_called_with("dummy_path", "w", encoding="utf-8")
        mock_json_dump.assert_called_once()


if __name__ == "__main__":
    unittest.main()
