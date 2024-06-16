CREATE TABLE IF NOT EXISTS calculator_entries (
    id SERIAL PRIMARY KEY,
    npr_expression VARCHAR(255) NOT NULL,
    expression VARCHAR(255) NOT NULL,
    result FLOAT NOT NULL
);