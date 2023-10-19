CREATE TABLE IF NOT EXISTS todo(
    todo_id INTEGER PRIMARY KEY,
    relative_todo_id INT DEFAULT 0,
    todo_time INT NULL,
    description INT NULL,
    by_user_id INT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_configuration(
    user_id INTEGER PRIMARY KEY,
    todo_dashboard_channel_id INT NULL,
    todo_dashboard_category_id INT NULL,
    should_notify_by_dm BOOLEAN NOT NULL CHECK (mycolumn IN (0, 1))
);

CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY
);

CREATE TRIGGER IF NOT EXISTS todo_add_relative_id_on_insert AFTER INSERT
    ON todo FOR EACH ROW
    BEGIN
        UPDATE
            todo
        SET
            relative_todo_id =
            (
                SELECT
                    MAX(relative_todo_id) + 1
                FROM
                    todo
                WHERE
                    by_user_id = NEW.by_user_id
            )
        WHERE
            todo_id = NEW.todo_id;
    END
;

CREATE TRIGGER IF NOT EXISTS todo_update_relative_id_on_delete AFTER DELETE
    ON todo FOR EACH ROW
    BEGIN
        UPDATE
            todo
        SET
            relative_todo_id = relative_todo_id - 1
        WHERE
            relative_todo_id > OLD.relative_todo_id;
    END
;
