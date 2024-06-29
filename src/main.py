from src.reports import main_reports
from src.services import main_services
from src.views import main_views


def main() -> None:
    """Вызов функции"""
    main_views()
    main_reports("Категория", "2024-06-22")
    main_services()


if __name__ == "__main__":
    main()
