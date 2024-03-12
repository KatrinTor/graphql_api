from graphql_query import Argument, Operation


def get_arguments(variables, variable):
    return [Argument(name=input_value, value=f"${input_value}")
            for k, v in variables.items()
            for input_value in variable
            if k == variable[0]]


def get_used_variables(variables, variable):
    return [variables[k]
            for k in variables.keys()
            for val in variable
            if k == val]


class ActionHandler:
    def __init__(self, used_variables, status_history):
        self.used_variables = used_variables
        self.status_history = status_history

    @staticmethod
    def make_mutation(used_variables, query):
        # рендер тела запроса для mutations
        operation = Operation(
            type="mutation",
            name="Mutation",
            variables=used_variables,
            queries=[query]
        )
        print(operation.render())
        return operation.render()

    @staticmethod
    def make_query(used_variables, query):
        # рендер тела запроса для query
        operation = Operation(
            type="query",
            name="Query",
            variables=used_variables,
            queries=[query]
        )
        print(operation.render())
        return operation.render()
