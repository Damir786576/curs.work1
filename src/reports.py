import json

import pandas as pd


def find_transactions(keyword: str) -> str:
    """
    Поиск транзакций по ключевому слову.
    """
    excel_path = "../data/operations.xls"
    sheet_data = pd.read_excel(excel_path)

    sheet_data["Описание"] = sheet_data["Описание"].astype(str)
    sheet_data["Категория"] = sheet_data["Категория"].astype(str)

    relevant_data = sheet_data[
        sheet_data["Описание"].str.contains(keyword, case=False)
        | sheet_data["Категория"].str.contains(keyword, case=False)
    ]

    transactions_found = relevant_data.to_dict(orient="records")

    if not transactions_found:
        transactions_found = [{"message": "Такой категории не найдено"}]

    json_output = json.dumps(transactions_found, indent=4, ensure_ascii=False)

    with open("search_results.json", "w", encoding="utf-8") as file:
        json.dump(transactions_found, file, indent=4, ensure_ascii=False)

    return json_output


def calculate_expenses(data_frame: pd.DataFrame, selected_category: str, date_for_report: pd.Timestamp) -> str:
    """
    Расчет расходов по выбранной категории.
    """
    data_frame["Дата платежа"] = pd.to_datetime(data_frame["Дата платежа"], format="%d.%m.%Y")

    relevant_expenses = data_frame[
        (data_frame["Категория"] == selected_category)
        & (data_frame["Дата платежа"] >= date_for_report - pd.DateOffset(months=3))
        & (data_frame["Дата платежа"] <= date_for_report)
    ]

    # Преобразование суммы расходов в float
    expenses_sum = relevant_expenses["Сумма платежа"].astype(float).sum()

    calculation_result = json.dumps(
        {
            "Категория": selected_category,
            "Общие расходы": expenses_sum,
            "Дата отчета": date_for_report.strftime("%Y-%m-%d"),
        },
        indent=4,
        ensure_ascii=False,
    )

    return calculation_result


def run_analysis(selected_category: str, date_for_report: str) -> None:
    """
    Запуск анализа транзакций и расчета расходов.
    """
    keyword = input("Введите ключевое слово для поиска: ")

    transactions_json = find_transactions(keyword)
    data_frame = pd.read_excel("../data/operations.xls")
    report_date = pd.to_datetime(date_for_report, format="%Y-%m-%d")
    expenses_json = calculate_expenses(data_frame, selected_category, report_date)

    print("Результаты поиска транзакций:", transactions_json)
    print("Результаты расчета расходов:", expenses_json)


run_analysis("Категория", "2024-06-22")
