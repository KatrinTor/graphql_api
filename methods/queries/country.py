from graphql_query import Variable, Query, Field

from methods.common_actions import get_arguments, get_used_variables, ActionHandler
from methods.api_request import api_request


class Request:

    def __init__(self, variable):
        # Определить переменные, необходимые для запроса
        variables = {
            "code": Variable(name="code", type="ID!")
        }

        # Сохранить предоставленную переменную и определить соответствующие аргументы и используемые переменные
        self.variable = variable
        self.arguments = get_arguments(variables, variable)
        self.used_variables = get_used_variables(variables, variable)

        # Конструктор запроса GraphQL для запроса, в который так же передаются arguments
        self.query = Query(
            name="country",
            arguments=self.arguments,
            fields=[
                "name",
                "native",
                "capital",
                "emoji",
                "currency",
                Field(
                    name="languages",
                    fields=[
                        "code",
                        "name"
                    ]
                )
            ]
        )

        # Сборка тела запроса
        self.result = ActionHandler.make_query(self.used_variables, self.query)

    def gql_request(self, **kwargs):
        # Отправка запроса GraphQL, используя сгенерированный запрос и предоставленные параметры/заголовки
        params = kwargs.pop("params", None)
        response = api_request("gql", json={"query": self.result, "variables": params})
        return response


class Variables:

    def __init__(self):
        self.data = {}

    def set_country_code(self, **kwargs):
        code = kwargs.pop("code", None)

        code_data = {}
        if code is not None:
            code_data["code"] = code

        self.data = code_data
        return self

    def build(self):
        return self.data
