-- Initialize the tasks table for the Task API
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
);

-- Insert sample data only if the table is empty
INSERT INTO tasks (title, done)
SELECT * FROM (VALUES
    ('Buy groceries', false),
    ('Complete assignment', true),
    ('Exercise for 30 minutes', false)
) AS v(title, done)
WHERE NOT EXISTS (SELECT 1 FROM tasks);
