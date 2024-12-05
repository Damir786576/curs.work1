# Course project

### Main Functions

### Home page
On the main page of the service users can get the following information in JSON format:
- A greeting corresponding to the current time of day.
- Data for each bank card:
  - Last 4 digits of the card.
  - Total amount of expenses.
  - Cashback (1 ruble for every 100 rubles).
- Top 5 transactions by payment amount.
- Exchange rate.
- Value of stocks from the S&P500 index.

### Services
#### Simple search
Spending by title

#### Counts
##### Spending by category
Spending by category

### Modules

### Module `views`
#### Functions:
- `welcome_message`: Returns a welcome message based on the time of day.
- `sum_expenses`: Calculates the amount of expenses from the list of transactions.
- `load_xlsx_data`: Loads data from an Excel file.
- `analyze_card_usage`: Analyzes card usage by transactions.
- `largest_transactions`: Returns the five largest transactions.
- `fetch_currency_value`: Retrieves the exchange rate of a currency against the ruble.
- `get_stock_currency`: Gets the current price of a stock.
- `execute_main`: The main function that performs data analysis.
- `save_to_json`: Saves the data to a JSON file.
- `run_application`: Starts the application.

### Module `reports`.
#### Functions:
- `find_transactions`: Searches for transactions by keyword and saves the results to a JSON file.
- `calculate_expenses`: Calculate expenses for the selected category for a certain period of time.
- `run_analysis`: Start analyzing transactions and calculating expenses, output the results to the console.

### Module `services`.
#### Functions:
- `read_transactions_xls`: Reads financial transactions from an XLSX file and returns them as a dictionary list.
- `search_by_description`: Searches for transactions matching the given query description and returns a list of transactions found.
- `write_to_json`: Writes the data to a JSON file, allowing you to easily transfer and store the search results.

#### Environment Variables.
- Can be got from the api.env file.