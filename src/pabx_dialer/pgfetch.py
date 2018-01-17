import psycopg2
from . import Registration, RegistrationSource

class PostgresRegistrationSource(RegistrationSource):
    """Postgres bound registration source
    """

    def __init__(self, connectionstring):
        RegistrationSource.__init__(self)
        self._connectionstring = connectionstring
        self._conn = psycopg2.connect(connectionstring)


    def get_pending_registrations(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, phonenumber FROM public.registrations WHERE processed = false ORDER BY id ASC LIMIT 100")
        rows = cursor.fetchall()
        for row in rows:
            yield Registration(row[0], row[1])


    def mark_as_processed(self, registrations):
        if(registrations is None):
            return
        cursor = self._conn.cursor()
        in_args = _collect_ids(registrations)
        if(in_args is None):
            return #empty collection
        sql = "UPDATE public.registrations SET Processed = true WHERE Id IN ({})".format(in_args)
        cursor.execute(sql)
        self._conn.commit()


    def close(self):
        self._conn.close()


def _collect_ids(registations):
    res = None
    for r in registations:
        if(res is None):
            res = str(r.reg_id)
        else:
            res = res + ", {}".format(r.reg_id)
    return res
