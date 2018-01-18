import ari
import logging
from pabx_dialer.pabx import PabxTarget
from pabx_dialer import Registration, RegistrationSource, CancellationTokenSource
from pabx_dialer.pgfetch import PostgresRegistrationSource

logging.basicConfig(level=logging.DEBUG)

#To: phone
# http://192.168.88.36:8088/ari/channels?endpoint=pjsip%2F0722421622%40%2B254709164000&app=channel-dump
# http://192.168.88.36:8088/ari/channels?endpoint=pjsip%2F0722421622%40%2B254709164000&app=bridge-hold&appArgs=registration
#To: extension
#http://192.168.88.36:8088/ari/channels?endpoint=pjsip%2F100&app=channel-dump
#http://192.168.88.36:8088/ari/channels?endpoint=pjsip%2F0722421622%40%2B254709164000&extension=100&callerId=system

class TestRegistrationSource(RegistrationSource):
    """Test
    """
    def __init__(self):
        RegistrationSource.__init__(self)

    def get_next_registration(self):
        yield Registration(1, "0722421622")

    def mark_as_processed(self, reg):
        print reg[0]

source = PostgresRegistrationSource("dbname='registrations' user='postgres' host='localhost' password='Dev-2010'")
target = PabxTarget("http://192.168.88.36:8088", "test", "test", "+254709164000")

reg = source.get_next_registration()
target.call(reg.phone_number, 109)
source.mark_as_processed(reg)
