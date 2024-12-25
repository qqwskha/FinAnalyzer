# src/main.py
from views import main_page_view
from datetime import datetime


def main():
    # Получаем текущую дату и время в нужном формате
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Используется текущая дата и время:", current_date)

    # Передаём текущую дату и время в main_page_view
    response = main_page_view(current_date)
    print(response)


if __name__ == '__main__':
    main()
