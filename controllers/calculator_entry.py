from services.postgres import PostgresDB, table_exists
from models.expression import CalculatorEntry


def insert_entry(db: PostgresDB, entry: CalculatorEntry):
    if not table_exists(db, "calculator_entries"):
        raise Exception("Table 'calculator_entries' does not exist.")

    db.create(
        "calculator_entries",
        ["NPR_expression", "expression", "result"],
        [entry.NPR_expression, entry.expression, entry.result],
    )
