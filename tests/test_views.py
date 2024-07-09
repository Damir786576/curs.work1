from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pandas as pd
import pytest
import requests

from src.views import (analyze_card_usage, fetch_currency_value, get_stock_currency, load_xlsx_data, save_to_json,
                       sum_expenses, welcome_message)


@pytest.fixture
def transactions_data() -> List[Dict[str, float]]:
    return [{"Сумма операции": -100.0}, {"Сумма операции": 200.0}, {"Сумма операции": -50.0}]


@pytest.fixture
def card_operations_data() -> List[Dict[str, float]]:
    return [{"Номер карты": 1234567890123456, "Сумма операции": -100.0, "Бонусы (включая кэшбэк)": 10.0}]


@pytest.mark.parametrize(
    "time, expected_message",
    [
        ("2024-06-22 09:00:00", "Доброе утро!"),
        ("2024-06-22 13:00:00", "Добрый день!"),
        ("2024-06-22 19:00:00", "Добрый вечер!"),
        ("2024-06-22 23:00:00", "Спокойной ночи!"),
        ("2024-06-22 03:00:00", "Спокойной ночи!"),
        ("2024-06-22 00:00:00", "Спокойной ночи!"),
        ("2024-06-22 05:00:00", "Доброе утро!"),
    ],
)
def test_welcome_message(time: str, expected_message: str) -> None:
    assert welcome_message(time) == expected_message


@pytest.mark.parametrize(
    "transactions, expected_sum",
    [
        ([{"Сумма операции": -100.0}, {"Сумма операции": 200.0}, {"Сумма операции": -50.0}], 150.0),
        ([{"Сумма операции": -20.0}, {"Сумма операции": -30.0}], 50.0),
        ([{"Сумма операции": -75.0}, {"Сумма операции": -25.0}, {"Сумма операции": 0.0}], 100.0),
        ([], 0.0),
        ([{"Сумма операции": 100.0}], 0.0),
        ([{"Сумма операции": -10.0}, {"Сумма операции": -90.0}, {"Сумма операции": -200.0}], 300.0),
    ],
)
def test_sum_expenses(transactions: List[Dict[str, float]], expected_sum: float) -> None:
    df = pd.DataFrame(transactions)
    assert sum_expenses(df) == expected_sum


@patch("pandas.read_excel")
def test_load_xlsx_data(mock_read_excel: Mock) -> None:
    mock_read_excel.return_value.to_dict.return_value = "mocked_data"
    assert load_xlsx_data("fake_path") == "mocked_data"


def test_analyze_card_usage(card_operations_data: List[Dict[str, Any]]) -> None:
    expected_result = [{"end_digits": "23456", "spent": 100.0, "bonus": 10.0}]
    actual_result = analyze_card_usage(card_operations_data)
    assert actual_result == expected_result


@patch("requests.get")
def test_fetch_currency_value(mock_get: Mock) -> Dict[str, float]:
    mock_response = {"conversion_rates": {"RUB": 75.0}}
    mock_get.return_value.json.return_value = mock_response
    value = fetch_currency_value("USD")
    assert value == 75.0
    return {"RUB": value}


@patch("yfinance.Ticker")
def test_get_stock_currency(mock_yfinance: Mock) -> Dict[str, float]:
    mock_yfinance.return_value.history.return_value = pd.DataFrame({"Close": [100.0]})
    value = get_stock_currency("AAPL")
    assert value == 100.0
    return {"AAPL": value}


@patch("json.dump")
def test_save_to_json(mock_json_dump: Mock) -> None:
    save_to_json({"test": "data"}, "fake_path")
    mock_json_dump.assert_called_once()


def test_welcome_message_exception_handling() -> None:
    with pytest.raises(ValueError):
        welcome_message("некорректный формат времени")


def test_sum_expenses_no_column():
    df = pd.DataFrame([{"Не Сумма операции": -100.0}])
    assert sum_expenses(df) == 0.0


def test_sum_expenses_empty_df():
    df = pd.DataFrame([])
    assert sum_expenses(df) == 0.0


@patch("requests.get")
def test_fetch_currency_value_exception_handling(mock_get: Mock) -> None:
    mock_get.side_effect = requests.exceptions.RequestException
    with pytest.raises(requests.exceptions.RequestException):
        fetch_currency_value("USD")


def test_sum_expenses_no_transactions():
    df = pd.DataFrame([{"Сумма операции": 0.0}])
    assert sum_expenses(df) == 0.0


def test_analyze_card_usage_multiple_cards(card_operations_data: List[Dict[str, Any]]):
    card_operations_data.extend([
        {"Номер карты": 1234567890123457, "Сумма операции": -200.0, "Бонусы (включая кэшбэк)": 20.0},
        {"Номер карты": 1234567890123458, "Сумма операции": -300.0, "Бонусы (включая кэшбэк)": 30.0}
    ])
    expected_result = [
        {"end_digits": "23456", "spent": 100.0, "bonus": 10.0},
        {"end_digits": "23457", "spent": 200.0, "bonus": 20.0},
        {"end_digits": "23458", "spent": 300.0, "bonus": 30.0}
    ]
    actual_result = analyze_card_usage(card_operations_data)
    assert actual_result == expected_result


def test_sum_expenses_negative_values_only():
    df = pd.DataFrame([{"Сумма операции": -100.0}, {"Сумма операции": -200.0}])
    assert sum_expenses(df) == 300.0


def test_welcome_message_unreachable_code():
    with pytest.raises(Exception):
        welcome_message("2024-06-22 24:00:00")


if __name__ == "__main__":
    pytest.main()
