from typing import Any, List, Optional, Tuple

try:
    import psycopg as psycopg
    PSYCOPG_VER = 3
except ImportError:
    import psycopg2 as psycopg
    import psycopg2.extensions
    PSYCOPG_VER = 2

from dslr.console import console

from .config import settings


class PGClient:
    """
    Thin wrapper around psycopg2
    """

    def __init__(self, host, port, user, password, dbname):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname

        self.conn = psycopg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
        )
        if PSYCOPG_VER == 2:
            self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        else:
            self.conn.set_autocommit(True)

        self.cur = self.conn.cursor()

    def execute(self, sql, data) -> Optional[List[Tuple[Any, ...]]]:
        if settings.debug:
            console.log(f"SQL: {sql}")
            console.log(f"DATA: {data}")

        self.cur.execute(sql, data)

        try:
            result = self.cur.fetchall()
        except psycopg.ProgrammingError:
            result = None

        return result
