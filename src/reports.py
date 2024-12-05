import json  # import library JSON for work with it.
import logging  # import the logging library for logging tasks.

import pandas as pd  # import pandas for data processing and analysis.

# Logging Setup
logging.basicConfig(filename="reports.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


# Search for transactions by keyword.
def find_transactions(keyword: str) -> str:
    try:
        # Search the file we're going to write the information.
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

        # Write that the category the person is looking for does not exist.
        if not transactions_found:
            transactions_found = [{"message": "Такой категории не найдено"}]
            logging.warning("Транзакции по ключевому слову не найдены.")

        json_output = json.dumps(transactions_found, indent=4, ensure_ascii=False)
        logging.info("Транзакции успешно преобразованы в JSON.")

        # Write the result to a json file
        with open("results_reports.json", "w", encoding="utf-8") as file:
            json.dump(transactions_found, file, indent=4, ensure_ascii=False)
            logging.info("Результаты поиска записаны в файл results_reports.json.")
        return json_output
    # if there's a mistake, we tell the person.
    except Exception as e:
        logging.error(f"Ошибка при поиске транзакций: {e}")
        raise


# Calculation of expenditures for the selected category.
def calculate_expenses(data_frame: pd.DataFrame, selected_category: str, date_for_report: pd.Timestamp) -> str:
    try:
        # Convert Payment Date to datetime format.
        data_frame["Дата платежа"] = pd.to_datetime(data_frame["Дата платежа"], format="%d.%m.%Y")
        logging.info("Дата платежа преобразована в формат datetime.")

        # Write down the expenses for the last 3 months.
        relevant_expenses = data_frame[
            (data_frame["Категория"] == selected_category)  # Filter by category.
            & (data_frame["Дата платежа"] >= date_for_report - pd.DateOffset(months=3))  # Last 3 months.
            & (data_frame["Дата платежа"] <= date_for_report)  # Up to the given date.
            ]

        # Sum the payment amounts.
        expenses_sum = relevant_expenses["Сумма платежа"].astype(float).sum()
        logging.info(f"Расходы по категории {selected_category} рассчитаны.")

        # Create JSON result.
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

        # write an error if it occurs
        return calculation_result
    except Exception as e:
        logging.error(f"Ошибка при расчете расходов: {e}")
        raise


# Run transaction analysis and costing.
def main_reports(selected_category: str, date_for_report: str) -> None:
    try:
        # Prompt user for a keyword for searching transactions.
        keyword = input("Введите ключевое слово для поиска: ")
        logging.info(f"Получено ключевое слово для поиска: {keyword}")

        # Find transactions based on the keyword.
        transactions_json = find_transactions(keyword)
        logging.info("Поиск транзакций выполнен.")

        data_frame = pd.read_excel("../data/operations.xls")
        logging.info("Файл Excel для анализа расходов успешно прочитан.")

        report_date = pd.to_datetime(date_for_report, format="%Y-%m-%d")
        logging.info(f"Дата отчета преобразована в формат datetime: {report_date}")

        # Calculate expenses for the selected category
        expenses_json = calculate_expenses(data_frame, selected_category, report_date)
        logging.info("Расчет расходов выполнен.")

        # Print the results of the transaction search and expense calculation.
        print("Результаты поиска транзакций:", transactions_json)
        print("Результаты расчета расходов:", expenses_json)
    except Exception as e:
        logging.error(f"Ошибка в функции main_reports: {e}")
        raise


if __name__ == "__main__":
    main_reports("Категория", "2024-06-22")
