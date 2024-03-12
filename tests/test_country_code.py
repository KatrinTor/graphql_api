import allure
import pytest

from methods.queries import country

country_codes = [
    {"code": "BR", "country_name": "Brazil"},
    {"code": "BY", "country_name": "Belarus"},
    {"code": "AG", "country_name": "Antigua and Barbuda"},
    {"code": "MA", "country_name": "Morocco"}
]


@pytest.mark.parametrize("country_code", country_codes)
@allure.title("Проверка соответствия страны заданному коду")
def test_country_code(country_code):
    code = country_code["code"]
    name = country_code["country_name"]

    with allure.step("Отправить запрос с кодом страны"):
        arguments = ["code"]
        param = country.Variables()
        param.set_country_code(code=code)
        params = param.build()

        response = country.Request(arguments).gql_request(params=params)

    with allure.step("Проверить соответстриве страны коду"):
        country_name = response.json()["data"]["country"]["name"]
        assert country_name == name, "Название страны не соответствует ее коду"
