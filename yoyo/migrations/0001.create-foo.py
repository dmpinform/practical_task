# file: migrations/0001.create-foo.py
from yoyo import step

__depends__ = {}


def apply_step(conn):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE foo (id INT, bar VARCHAR(20), PRIMARY KEY (id))"
    )


def rollback_step(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE foo")


steps = [step(apply_step, rollback_step)]
