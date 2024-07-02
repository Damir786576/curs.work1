import json
import logging

import pandas as pd

# Настройка логирования
logging.basicConfig(filename="reports.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


def find_transactions(keyword: str) -> str:
    """Поиск транзакций по ключевому слову."""
    try:
        excel_path = "../data/operations.xls"
        sheet_data = pd.read_excel(excel_path)
        logging.info("Файл Excel успешно прочитан.")

        sheet_data["Описание"] = sheet_data["Описание"].astype(str)
        sheet_data["Категория"] = sheet_data["Категория"].astype(str)

        relevant_data = sheet_data[
            sheet_data["Описание"].str.contains(keyword, case=False)
            | sheet_data["Категория"].str.contains(keyword, case=False)
        ]

        transactions_found = relevant_data.to_dict(orient="records")

        if not transactions_found:
            transactions_found = [{"message": "Такой категории не найдено"}]
            logging.warning("Транзакции по ключевому слову не найдены.")

        json_output = json.dumps(transactions_found, indent=4, ensure_ascii=False)
        logging.info("Транзакции успешно преобразованы в JSON.")

        with open("results_reports.json", "w", encoding="utf-8") as file:
            json.dump(transactions_found, file, indent=4, ensure_ascii=False)
            logging.info("Результаты поиска записаны в файл results_reports.json.")

        return json_output
    except Exception as e:
        logging.error(f"Ошибка при поиске транзакций: {e}")
        raise


def calculate_expenses(data_frame: pd.DataFrame, selected_category: str, date_for_report: pd.Timestamp) -> str:
    """Расчет расходов по выбранной категории."""
    try:
        data_frame["Дата платежа"] = pd.to_datetime(data_frame["Дата платежа"], format="%d.%m.%Y")
        logging.info("Дата платежа преобразована в формат datetime.")

        relevant_expenses = data_frame[
            (data_frame["Категория"] == selected_category)
            & (data_frame["Дата платежа"] >= date_for_report - pd.DateOffset(months=3))
            & (data_frame["Дата платежа"] <= date_for_report)
        ]

        expenses_sum = relevant_expenses["Сумма платежа"].astype(float).sum()
        logging.info(f"Расходы по категории {selected_category} рассчитаны.")

        calculation_result = json.dumps(
            {
                "Категория": selected_category,
                "Общие расходы": expenses_sum,
                "Дата отчета": date_for_report.strftime("%Y-%m-%d"),
            },
            indent=4,
            ensure_ascii=False,
        )
        logging.info("Расходы успешно преобразованы в JSON.")

        return calculation_result
    except Exception as e:
        logging.error(f"Ошибка при расчете расходов: {e}")
        raise


def main_reports(selected_category: str, date_for_report: str) -> None:
    """Запуск анализа транзакций и расчета расходов."""
    try:
        keyword = input("Введите ключевое слово для поиска: ")
        logging.info(f"Получено ключевое слово для поиска: {keyword}")

        transactions_json = find_transactions(keyword)
        logging.info("Поиск транзакций выполнен.")

        data_frame = pd.read_excel("../data/operations.xls")
        logging.info("Файл Excel для анализа расходов успешно прочитан.")

        report_date = pd.to_datetime(date_for_report, format="%Y-%m-%d")
        logging.info(f"Дата отчета преобразована в формат datetime: {report_date}")

        expenses_json = calculate_expenses(data_frame, selected_category, report_date)
        logging.info("Расчет расходов выполнен.")

        print("Результаты поиска транзакций:", transactions_json)
        print("Результаты расчета расходов:", expenses_json)
    except Exception as e:
        logging.error(f"Ошибка в функции main_reports: {e}")
        raise


if __name__ == "__main__":
    main_reports("Категория", "2024-06-22")
