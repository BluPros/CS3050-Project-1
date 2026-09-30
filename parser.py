import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pyparsing as pp
from pyparsing import Keyword, Literal, Optional, Word, alphas, alphanums, pyparsing_common, ParseException, Group


# The parser takes a string and returns a dictionary of strings with the following form:
# {'condition1': {'field': (field), 'operator': (operator), 'value': (value)}, 'logic_op': None, 'condition2' : None}
# if there is no second condition. and
# {'condition1': {'field': (field), 'operator': (operator), 'value': (value)}, 'logic_op': (logic_op),
# 'condition2': {'field': (field), 'operator': (operator), 'value': (value)}}
# if there is a second condition.
#
# To use this result, do something along the lines of result["condition1"]["field"] or
# ["condition1"]["operator"] or ["condition2"]["value"] to get their respective strings.
#
# Note: fields will be checked for viability (i.e. they have to be an actual field),
#       but values are not. Something like "release_date=aaaaaa" will be considered valid.
# Note: Everything is returned as strings. If the string "price=1.99" is parsed,
#       ["condition1"]["value"] will be "1.99", not the float 1.99.
def parse(query_string: str):

    and_op = Keyword("and")
    or_op = Keyword("or")

    comparison_op = (
        Literal(">=") |
        Literal("<=") |
        Literal("!=") |
        Literal(">") |
        Literal("<") |
        Literal("=")
    )

    field = (
        Literal("app_id") |
        Literal("name") |
        Literal("release_date") |
        Literal("price") |
        Literal("metacritic_url") |
        Literal("categories") |
        Literal("genres") |
        Literal("tags")
    )

    value = Word(alphanums + '.' + '/' + '-')
    condition = Group(field("field") + comparison_op("operator") + value("value"))
    condition2 = Optional(Optional(or_op | and_op)("logic_op") + condition("condition2"))

    query = condition("condition1") + condition2 + pp.StringEnd()
    try:
        result = query.parse_string(query_string)
        parsed_result = {
            "condition1": {
                "field": result["condition1"]["field"],
                "operator": result["condition1"]["operator"],
                "value": result["condition1"]["value"]
            },
            "logic_op": None,
            "condition2": None
        }
        if "condition2" in result:
            if "logic_op" in result:
                parsed_result["logic_op"] = result["logic_op"]
            else: # makes the dict return an and even if implied and was used
                parsed_result["logic_op"] = "and"

            parsed_result["condition2"] = {
                "field": result["condition2"]["field"],
                "operator": result["condition2"]["operator"],
                "value": result["condition2"]["value"]
            }

        return parsed_result
    except ParseException as e:

        return None


