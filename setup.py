from services.postgres import PostgresDB

db = PostgresDB(host="0.0.0.0")

db.setup(
    "calculator_db",
    "calculator_entries",
    ["NPR_expression", "expression", "result"],
    ["VARCHAR(255)", "VARCHAR(255)", "FLOAT"],
)
