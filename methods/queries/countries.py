from graphql_query import Variable, Query

from methods.api_request import api_request
from methods.common_actions import (get_arguments,
                                    get_used_variables,
                                    ActionHandler)


class Request:

    def __init__(self, variable):
        variables = {
            "filter": Variable(name="filter", type="CountryFilterInput")}

        self.variable = variable
        self.arguments = get_arguments(variables, variable)
        self.used_variables = get_used_variables(variables, variable)

        self.query = Query(
            name="countries",
            arguments=self.arguments,
            fields=[
                "name",
                "code",
                "currency"
            ]
        )

        self.result = ActionHandler.make_query(self.used_variables, self.query)

    def gql_request(self, **kwargs):
        params = kwargs.pop("params", None)
        response = api_request("gql",
                               json={"query": self.result,
                                     "variables": params})
        return response


class Variables:

    def __init__(self):
        self.data = {}

    def set_filter_data(self, **kwargs):
        letter = kwargs.pop("letter", None)

        filter_data = {}
        if letter is not None:
            filter_data["regex"] = f"{letter}"
        self.data = {"filter": {"name": filter_data}}
        return self

    def build(self):
        return self.data
