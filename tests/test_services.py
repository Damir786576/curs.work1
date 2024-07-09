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


@patch("pandas.read_excel")
def test_read_transactions_xls_empty_file(mock_read_excel: Any) -> None:
    mock_read_excel.return_value.to_dict.return_value = {}
    mock_read_excel.return_value.to_dict.side_effect = lambda orient: [] if orient == "records" else {}
    result = read_transactions_xls("dummy_path")
    assert result == []


@patch("pandas.read_excel")
def test_read_transactions_xls_file_not_found(mock_read_excel: Any) -> None:
    mock_read_excel.side_effect = FileNotFoundError("Файл не найден")
    with pytest.raises(FileNotFoundError):
        read_transactions_xls("non_existent_path")


@patch("logging.info")
def test_logging_on_successful_read(mock_logging_info: Any, sample_transactions: List[Dict[str, Any]]) -> None:
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value.to_dict.return_value = sample_transactions
        read_transactions_xls("dummy_path")
        mock_logging_info.assert_called_with("Транзакции успешно прочитаны из файла.")


@pytest.mark.parametrize(
    "query, expected_count",
    [
        ("", 0),
        ("Не существующее описание", 0),
    ],
)
def test_search_by_description_edge_cases(
    sample_transactions: List[Dict[str, Any]], query: str, expected_count: int
) -> None:
    result = search_by_description(sample_transactions, query)
    assert len(result) == expected_count, f"Ожидалось {expected_count}, получено {len(result)}"


def test_read_transactions_xls_exception_handling() -> None:
    with pytest.raises(Exception):
        read_transactions_xls("invalid_path")


def test_write_to_json_exception_handling(sample_transactions: List[Dict[str, Any]]) -> None:
    with pytest.raises(Exception):
        write_to_json("/invalid_path", sample_transactions)


@patch("logging.error")
def test_logging_on_error(mock_logging_error: Any) -> None:
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.side_effect = Exception("Ошибка")
        try:
            read_transactions_xls("dummy_path")
        except Exception:
            pass
        mock_logging_error.assert_called_with("Ошибка при чтении файла: Ошибка")


if __name__ == "__main__":
    pytest.main()
