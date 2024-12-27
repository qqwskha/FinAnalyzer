import pandas as pd
import logging
from services import analyze_cashback_categories

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Загрузка данных
        data = pd.read_excel('../data/operations.xlsx')
        logger.info("Транзакции успешно загружены.")
    except Exception as e:
        logger.error(f"Ошибка загрузки данных: {e}")
        return

    # Анализ категорий кешбэка
    year = 2021
    month = 12
    cashback_analysis = analyze_cashback_categories(data, year, month)

    if cashback_analysis:
        pd.DataFrame(list(cashback_analysis.items()), columns=['Категория', 'Сумма кешбэка']) \
            .to_csv('cashback_analysis.csv', index=False)
        logger.info("Результаты анализа сохранены в cashback_analysis.csv")
    else:
        logger.warning("Нет данных для анализа кешбэка.")

if __name__ == "__main__":
    main()
