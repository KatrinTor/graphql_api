import string

import allure
import pytest

from methods.queries import countries


@pytest.mark.parametrize("letter", string.ascii_uppercase)
@allure.title("Фильтр по первой букве страны выводит соответствующие странны")
def test_country_name_filter(letter):
    """
    Тест проверяет, что поиск по букве выдает страны,
    в названии которых хотя бы одно слово начинается с этой букве.
    """
    with allure.step(f"Отправить запрос c буквой {letter} в фильтрe"):
        arguments = ["filter"]
        param = countries.Variables()
        param.set_filter_data(letter=letter)
        params = param.build()

        response = countries.Request(arguments).gql_request(params=params)

    with allure.step(f"Проверка: в названии страны содержится слово на букву '{letter}'"):
        objects = response.json()["data"]["countries"]
        for object in objects:
            words = object["name"].split()
            for word in words:
                if word.startswith(letter) is False:
                    print(f'Ошибка: по фильтру {letter} выводится {object["name"]}')
