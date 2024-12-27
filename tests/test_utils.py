from datetime import datetime

from src.utils import get_greeting


def test_get_greeting():
    assert get_greeting(datetime(2024, 6, 25, 8)) == "Доброе утро"
    assert get_greeting(datetime(2024, 6, 25, 14)) == "Добрый день"
    assert get_greeting(datetime(2024, 6, 25, 20)) == "Добрый вечер"
    assert get_greeting(datetime(2024, 6, 25, 3)) == "Доброй ночи"
