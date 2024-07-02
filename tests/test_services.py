from typing import Any, Dict, List
from unittest.mock import patch

import pytest

from src.services import read_transactions_xls, search_by_description, write_to_json


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"Описание": "Перевод средств", "Сумма": 1000},
        {"Описание": "Оплата услуг", "Сумма": 2000},
        {"Описание": "Перевод средств", "Сумма": 1500},
    ]


@pytest.mark.parametrize(
    "query, expected_count",
    [
        ("Перевод средств", 2),
        ("Оплата услуг", 1),
    ],
)
def test_search_by_description(sample_transactions: List[Dict[str, Any]], query: str, expected_count: int) -> None:
    result = search_by_description(sample_transactions, query)
    assert len(result) == expected_count
    assert all(transaction["Описание"] == query for transaction in result)


@patch("pandas.read_excel")
def test_read_transactions_xls(mock_read_excel: Any, sample_transactions: List[Dict[str, Any]]) -> None:
    mock_read_excel.return_value.to_dict.return_value = sample_transactions
    result = read_transactions_xls("dummy_path")
    assert result == sample_transactions


@patch("builtins.open")
@patch("json.dump")
def test_write_to_json(mock_json_dump: Any, mock_open: Any, sample_transactions: List[Dict[str, Any]]) -> None:
    write_to_json("dummy_path", sample_transactions)
    mock_open.assert_called_with("dummy_path", "w", encoding="utf-8")
    mock_json_dump.assert_called_once()


if __name__ == "__main__":
    pytest.main()
