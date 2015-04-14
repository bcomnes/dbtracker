import psycopg2
import logging

logger = logging.getLogger(__name__)


class Database(object):

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        # From
        # https://github.com/PSU-OIT-ARC/django-arcutils/blob/master/arcutils/__init__.py#L82
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()]

    def count_rows(self):
        pass

    def connection(self):
        raise NotImplementedError

    def get_tables(self):
        raise NotImplementedError

    def query_for_tables(self, cursor):
        raise NotImplementedError


class Mysql(Database):

    def __init__(self, host, user, password):
        super().__init__(host, user, password)

    def connection(self, action):
        logger.info('Collecting mySQL stats')
        try:
            with pymysql.connect(self.host, self.user, self.password) as conn:
                with conn.cursor() as cursor:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        action(cursor)
        except pymysql.err.OperationalError as e:
            logger.error("mySQL error: %s" % e)

    def get_tables(self):
        return connection(self.query_for_tables)

    def query_for_tables(self, cursor):
        cursor.execute("SELECT * FROM information_schema.tables \
            WHERE \TABLE_TYPE != 'VIEW'")
        tables = self.dictfetchall(cursor)
        tables = self.count_rows(cursor, tables)
        logger.info('mySQL stats collected')
        return tables

    def count_rows(self, cursor, tables):
        for table in tables:
            try:
                cursor.execute(
                    "SELECT COUNT(*) FROM `%(db)s`.`%(table)s`" %
                    {"db": table.get("TABLE_SCHEMA"),
                     "table": table.get("TABLE_NAME")})
                row_count = dictfetchall(cursor)[0]['COUNT(*)']
            except pymysql.err.InternalError as err:
                logger.warning('Skipping: %s', "{}.{}".format(
                    table.get("TABLE_SCHEMA"), table.get("TABLE_NAME")),
                    extra={'err': err})
            finally:
                table['row_count'] = row_count or 0
            return tables


class Postgres(Database):

    def __init__(self, host, user, password):
        super().__init__(host, user, password)

    def connection(self, database, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with psycopg2.connect(self.host, self.user, self.password,
                                      database=database) as conn:
                    with conn.cursor() as cursor:
                        action(cursor)
            except:
                logger.error("Error connecting to postgreSQL")

    def get_dbs(self):

    def get_tables(self):
        dbs = self.get_db()
        for db in dbs:
            connection(get_


class Storage(Postgres):

    def __init__(self, host, user, password):
        super().__init__(host, user, password)

    def insert(self, date_time, db_provider, db_name, schema_name, table_name, row_count):
        with self._conn:

    def save_db_dump(self):
        pass

    def get_history(self):
        pass

    def get_timestamp(self):
        pass
