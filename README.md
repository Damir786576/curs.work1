# Курсовой проект

## Основные функции

### Главная страница
На главной странице сервиса пользователи могут получить следующую информацию в формате JSON:
- Приветствие, соответствующее текущему времени суток.
- Данные по каждой банковской карте:
  - Последние 4 цифры карты.
  - Общая сумма расходов.
  - Кешбэк (1 рубль на каждые 100 рублей).
- Топ-5 транзакций по сумме платежа.
- Курс валют.
- Стоимость акций из индекса S&P500.

### Сервисы
#### Простой поиск
Траты по задоному описанию

#### Отсчеты
##### Траты по категории
Траты по заданым категориям

## Модули

### Модуль `views`
#### Функции:
- `welcome_message`: Возвращает приветственное сообщение в зависимости от времени суток.
- `sum_expenses`: Считает сумму расходов из списка операций.
- `load_xlsx_data`: Загружает данные из Excel файла.
- `analyze_card_usage`: Анализирует использование карт по операциям.
- `largest_transactions`: Возвращает пять самых крупных транзакций.
- `fetch_currency_value`: Получает курс валюты к рублю.
- `get_stock_currency`: Получает текущую цену акции.
- `execute_main`: Основная функция, выполняющая анализ данных.
- `save_to_json`: Сохраняет данные в JSON-файл.
- `run_application`: Запускает приложение.

### Модуль `reports`
#### Функции:
- `find_transactions`: Поиск транзакций по ключевому слову и сохранение результатов в JSON файл.
- `calculate_expenses`: Расчет расходов по выбранной категории за определенный период времени.
- `run_analysis`: Запуск анализа транзакций и расчета расходов, вывод результатов в консоль.

### Модуль `services`
#### Функции:
- `read_transactions_xls`: Читает финансовые транзакции из XLSX файла и возвращает их в виде списка словарей.
- `search_by_description`: Ищет транзакции, соответствующие данному описанию запроса, и возвращает список найденных транзакций.
- `write_to_json`: Записывает данные в JSON файл, что позволяет легко передавать и хранить результаты поиска.

### Переменные окружения
- Можно получить в файле api.env
