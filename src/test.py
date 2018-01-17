from __future__ import print_function
from pabx_dialer.pgfetch import PostgresRegistrationSource

str = "dbname='registrations' user='postgres' host='localhost' password='Dev-2010'"
src = PostgresRegistrationSource(str)
registrations = [r for r in src.get_pending_registrations()]
for r in registrations:
    print(r)

src.mark_as_processed(registrations)

