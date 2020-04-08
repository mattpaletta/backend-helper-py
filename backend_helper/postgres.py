import logging
from threading import Semaphore
from time import sleep

import psycopg2.pool


class ReallyThreadedConnectionPool(psycopg2.pool.ThreadedConnectionPool):
    def __init__(self, minconn: int, maxconn: int, *args, **kwargs):
        self.minconn = minconn
        self.maxconn = maxconn
        self._semaphore = Semaphore(maxconn)
        super().__init__(minconn, maxconn, *args, **kwargs)

    def cursor(self, cursor_factory):
        class temp_obj(object):
            def __init__(self, connection_pool: ReallyThreadedConnectionPool):
                self._pool = connection_pool
                self._curr_con = None
                self._curr_cursor = None

            def __enter__(self, *args, **kwargs):
                self._curr_con = self._pool.getconn(*args, **kwargs)
                self._curr_cursor = self._curr_con.cursor(cursor_factory = cursor_factory)
                return self._curr_cursor

            def __exit__(self, exc_type, exc_val, exc_tb):
                self._curr_cursor.close()
                self._pool.putconn(self._curr_con)

        return temp_obj(connection_pool = self)

    def getconn(self, *args, **kwargs):
        self._semaphore.acquire()
        return super().getconn(*args, **kwargs)

    def putconn(self, *args, **kwargs):
        super().putconn(*args, **kwargs)
        self._semaphore.release()


def connect(user: str,
            password: str,
            host: str,
            port: int,
            database: str,
            minconn: int = 1,
            maxconn: int = 20,
            max_retries: int = 100):
    postgres_pool = None
    pool_class = ReallyThreadedConnectionPool if maxconn > 1 else psycopg2.pool.SimpleConnectionPool
    for i in range(max_retries):
        try:
            # Give the database a change to initialize
            postgres_pool = pool_class(minconn = minconn,
                                       maxconn = maxconn,
                                       user = user,
                                       password = password,
                                       host = host,
                                       port = port,
                                       database = database)

            if postgres_pool:
                break

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error('Failure to connect to Postgres: ', error)
            sleep(2 * i)

    if not postgres_pool:
        logging.error('Failure to connect to Postgres')
        exit(1)
    return postgres_pool
