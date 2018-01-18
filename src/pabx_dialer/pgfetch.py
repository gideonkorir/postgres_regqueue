import psycopg2
from . import Registration, RegistrationSource

class PostgresRegistrationSource(RegistrationSource):
    """Postgres bound registration source
    """

    def __init__(self, connectionstring):
        RegistrationSource.__init__(self)
        self._connectionstring = connectionstring
        self._conn = psycopg2.connect(connectionstring)


    def get_next_registrations(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            UPDATE public.call_queue_creator SET lockedto = now()
            WHERE id in(
                SELECT id FROM public.call_queue_creator
                WHERE beencalled = false AND (lockedto IS NULL OR lockedto <= now())
                ORDER BY id ASC
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            )
            RETURNING id,phonenumber
        """)
        row = cursor.fetch()
        if row is None:
            return None
        else:
            return Registration(row[0], row[1])


    def mark_as_processed(self, registration):
        if(registration is None):
            return
        sql = "UPDATE public.call_queue_creator SET beencalled = true WHERE Id= {}".format(registration.reg_id)
        cursor = self._conn.cursor()
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
