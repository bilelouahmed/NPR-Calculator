import math

import argparse

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI()


class ExpressionRequest(BaseModel):
    expression: str


def calculator(expression: str, verbose=False) -> tuple[float, str]:
    fifo = []
    classic_exp_fifo = []

    tokens = expression.split(" ")

    for token in tokens:
        if token == "":
            continue

        if token.isdigit() or (token[0] == "-" and token[1:].isdigit()):
            fifo.append(float(token))
            classic_exp_fifo.append(token)

            if verbose:
                print(f"Push: {token}\t---> Pile: {fifo}")

        elif token in ["sin", "cos", "tan", "exp"]:
            if len(fifo) < 1:
                raise HTTPException(
                    status_code=400,
                    detail="Bad Request : The stack should contain at least one operand before a unary operator.",
                )

            a = fifo.pop()
            first_operand = classic_exp_fifo.pop()

            if verbose:
                print(f"Pop: {a} for operator '{token}'")

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
                    f"Résultat de {token}({first_operand}) = {result}\t---> Pile: {fifo}"
                )

        else:
            if len(fifo) < 2:
                raise HTTPException(
                    status_code=400,
                    detail="Bad Request : The stack should contain at least two operands before a binary operator.",
                )

            b = fifo.pop()
            a = fifo.pop()
            second_operand = classic_exp_fifo.pop()
            first_operand = classic_exp_fifo.pop()

            if verbose:
                print(f"Pop: {a} et {b} for operator '{token}'")

            if token == "+":
                result = a + b
            elif token == "-":
                result = a - b
            elif token == "*":
                result = a * b
            elif token == "/":
                if b == 0:
                    raise HTTPException(
                        status_code=400, detail="Bad Request : Division per zero."
                    )
                result = a / b
            elif token == "^":
                result = a**b
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Bad Request : Unknown operator '{token}'. Please, check the README file.",
                )

            fifo.append(result)
            classic_exp_fifo.append(f"({first_operand} {token} {second_operand})")

            if verbose:
                print(f"Result of {a} {token} {b} = {result}\t---> Pile: {fifo}")

    if len(fifo) != 1:
        raise HTTPException(
            status_code=400,
            detail="Bad Request : The expression is not valid. It should normally contain only one element in the stack at the end.",
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
        help="Verbose mode. Default is False.",
    )

    args = parser.parse_args()

    VERBOSE = args.verbose

    @app.post("/calculator")
    async def main(request: ExpressionRequest):
        expression = request.expression

        if not expression:
            raise HTTPException(
                status_code=400,
                detail="Bad Request : Please, provide at least the field: expression.",
            )

        if not isinstance(expression, str):
            raise HTTPException(
                status_code=400,
                detail="Bad Request : Please, check you typed well your fields (expression: str).",
            )

        result, classic_expression = calculator(expression, verbose=VERBOSE)

        return {"result": result, "expression": classic_expression}

    uvicorn.run(app, host="0.0.0.0", port=6000)
