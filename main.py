import math
import argparse

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)


def calculator(expression: str, verbose=False) -> tuple["float", "str"]:
    fifo = []
    classic_exp_fifo = []

    tokens = expression.split(" ")

    if tokens == [""]:
        raise BadRequest("Error : The expression is empty.")

    for token in tokens:

        if token.isdigit() or (token[0] == "-" and token[1:].isdigit()):
            fifo.append(float(token))
            classic_exp_fifo.append(token)

            if verbose:
                print(f"Push : {token}\t---> Pile : {fifo}")

        elif token in ["sin", "cos", "tan", "exp"]:
            if len(fifo) < 1:
                raise BadRequest(
                    "Error : The stack should contain at least one operand before a unary operator."
                )

            a = fifo.pop()
            first_operand = classic_exp_fifo.pop()

            if verbose:
                print(f"Pop : {a} for operator '{token}'")

            if token == "sin":
                result = math.sin(a)
            elif token == "cos":
                result = math.cos(a)
            elif token == "tan":
                result = math.tan(a)
            elif token == "exp":
                result = math.exp(a)

            fifo.append(result)
            classic_exp_fifo.append(f"{token}({first_operand})")

            if verbose:
                print(
                    f"Résultat de {token}({first_operand}) = {result}\t---> Pile : {fifo}"
                )

        else:
            if len(fifo) < 2:
                raise BadRequest(
                    "Error : The stack should contain at least two operands before a binary operator."
                )

            b = fifo.pop()
            a = fifo.pop()
            second_operand = classic_exp_fifo.pop()
            first_operand = classic_exp_fifo.pop()

            if verbose:
                print(f"Pop : {a} et {b} for operator '{token}'")

            if token == "+":
                result = a + b
            elif token == "-":
                result = a - b
            elif token == "*":
                result = a * b
            elif token == "/":
                if b == 0:
                    raise BadRequest("Error : Division per zero.")
                result = a / b
            elif token == "^":
                result = a**b
            else:
                raise BadRequest(
                    f"Error : Unknown operator '{token}'. Please, check the README file."
                )

            fifo.append(result)
            classic_exp_fifo.append(f"({first_operand} {token} {second_operand})")

            if verbose:
                print(f"Result of {a} {token} {b} = {result}\t---> Pile : {fifo}")

    if len(fifo) != 1:
        raise BadRequest(
            "Error : The expression is not valid. It should normally contain only one element in the stack at the end."
        )

    return fifo[0], classic_exp_fifo[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="API for a Reverse Polish Notation calculator."
    )
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        help=f"Verbose mode. Default is False.",
    )

    args = parser.parse_args()

    VERBOSE = args.verbose

    @app.post("/calculator")
    def main():
        expression = request.json["expression"]

        if not (expression):
            raise BadRequest("Please, provide at least with field : expression.")

        if not (type(expression) == str):
            raise BadRequest(
                "Please, check you typed well your fields (expression : str)."
            )

        if set(request.json.keys()) - {"expression"}:
            raise BadRequest(
                "An extra field has been received. Please, check you provide your request with at most this argument : expression (str)."
            )

        result, classic_expression = calculator(expression, verbose=VERBOSE)

        return jsonify({"result": result, "expression": classic_expression})

    app.run(host="0.0.0.0", port=6000)
