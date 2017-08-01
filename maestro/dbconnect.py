'''
Inspired by: USGS-EROS/espa-api/blob/master/api/util/dbconnect.py (LICENSE NASA-1.3)
'''
import os

import psycopg2
import psycopg2.extras as db_extras

MAESTRO_PGHOST = os.environ.get('MAESTRO_PGHOST', 'localhost')
MAESTRO_PGDB = os.environ.get('MAESTRO_PGDB', 'postgres')
MAESTRO_PGTAB = os.environ.get('MAESTRO_PGTAB', 'postgres')


class DBConnect(object):
    def __init__(self, host=None, dbname=None):
        conn = psycopg2.connect("host={} dbname={} user=postgres"
                                .format(host or MAESTRO_PGHOST,
                                        dbname or MAESTRO_PGDB))
        self.cur = conn.cursor(cursor_factory=db_extras.DictCursor)

    def get_work(self, n_records=50):
        self.cur.execute("SELECT * FROM {} LIMIT {};"
                         .format(None or MAESTRO_PGTAB,
                                 n_records))
        work = self.cur.fetchall()
        print(work[0].keys())
        return [(w['unitid'], w['unitname']) for w in work]


db_instance = DBConnect()
