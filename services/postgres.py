import psycopg2
from psycopg2 import sql


class PostgresDB:
    def __init__(
        self,
        dbname: str = "postgres",
        user: str = "postgres",
        password: str = "postgres",
        host: str = "localhost",
        port: int = 5432,
    ):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query: str, params: list = None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()

    def fetch_query(self, query: str, params: list = None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def create(self, table: str, columns: list, values: list):
        columns_str = ", ".join(columns)
        values_template = ", ".join(["%s"] * len(values))
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table), sql.SQL(columns_str), sql.SQL(values_template)
        )
        self.execute_query(query, values)

    def read(self, table: str, columns: list = None, condition: str = None):
        columns_str = (
            sql.SQL(", ").join(map(sql.Identifier, columns))
            if columns
            else sql.SQL("*")
        )
        query = sql.SQL("SELECT {} FROM {}").format(columns_str, sql.Identifier(table))
        if condition:
            query += sql.SQL(" WHERE {}").format(sql.SQL(condition))
        return self.fetch_query(query)

    def update(self, table: str, set_values: dict, condition: str):
        set_clause = sql.SQL(", ").join(
            sql.SQL("{} = %s").format(sql.Identifier(column))
            for column in set_values.keys()
        )
        query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
            sql.Identifier(table), set_clause, sql.SQL(condition)
        )
        self.execute_query(query, list(set_values.values()))

    def delete(self, table: str, condition: str):
        query = sql.SQL("DELETE FROM {} WHERE {}").format(
            sql.Identifier(table), sql.SQL(condition)
        )
        self.execute_query(query)

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def setup(self, dbname: str, table_name: str, columns: list, types: list):
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {dbname};"
        self.execute_query(create_database_query)

        self.conn.close()
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=self.conn.user,
            password=self.conn.password,
            host=self.conn.host,
            port=self.conn.port,
        )
        self.cursor = self.conn.cursor()

        if not table_exists(self, table_name):
            columns_str = ", ".join(
                [f"{column} {type}" for column, type in zip(columns, types)]
            )
            create_table_query = f"CREATE TABLE {table_name} ({columns_str});"
            self.execute_query(create_table_query)


def table_exists(db: PostgresDB, table_name: str) -> bool:
    query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
    return db.fetch_query(query)[0][0]
