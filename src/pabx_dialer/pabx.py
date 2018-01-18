import ari
import logging
import time
from . import Registration

logging.basicConfig(level=logging.DEBUG)

#To: extension
#http://192.168.88.36:8088/ari/channels?endpoint=pjsip%2F0722421622%40%2B254709164000&extension=100&callerId=system

PJSIP = "PJSIP"



class AvailableResource(object):
    """Represents a pabx resource that is callable
    """
    _technology = None
    _resource = None

    def __init__(self, technology, resource):
        self._technology = technology
        self._resource = resource

    @property
    def technology(self):
        """The technology of the pabx resource
        """
        return self._technology

    @property
    def resource(self):
        """id of the resource under the technology
        """
        return self._resource


def is_available_endpoint(endpoint, technology_check):
    """Checks to see if we can call the endpoint
    """
    other_ok = endpoint.json['state'] == "online" and len(endpoint.json['channel_ids']) == 0 and len(endpoint.json['resource']) == 3
    if other_ok:
        if technology_check is not None:
            other_ok = technology_check(endpoint.json['technology'])
    return other_ok


def is_pjsip(technology):
    """checks if technology string corresponds to pjsip
    """
    return technology == 'PJSIP'

def full_resource_id(technology, resourceId):
    """Get full resource of a pabx resource
    """
    return "{}/{}".format(technology, resourceId)

class PabxTarget(object):
    """Target to make calls on pending registrations
    """

    _client = None
    _outbound_src_id = None #the number to use to dial out e.g. when calling 07x from 07y sf line we do 07x@07y
    _caller_id = None
    _sleep_inteval = 5

    def __init__(self, ari_url, ari_username, ari_password, outbound_src_id, caller_id = "registrations", sleep_interval = 5):
        self._client = ari.connect(ari_url, ari_username, ari_password)
        self._outbound_src_id = outbound_src_id
        self._caller_id = caller_id
        self._sleep_inteval = sleep_interval

    def _get_resources(self):
        endpoints = self._client.endpoints.list()
        #endpoint { technology:pjsip, "resource":"ext", "state":"online", "channel_ids": [] }
        available = [AvailableResource(endpoint.json['technology'], endpoint.json['resource']) for endpoint in endpoints if is_available_endpoint(endpoint, is_pjsip)]
        return available

    def _get_outbound_endpoint(self, reg_number):
        return full_resource_id(PJSIP, "{}@{}".format(reg_number, self._outbound_src_id))

    def call(self, phone_number, extension):
        """we call this to make calls
           trunk_phone - the phone to use when calling out
           phone_number to call
        """
        endpoint = self._get_outbound_endpoint(phone_number)
        self._client.channels.originate(endpoint = endpoint, callerId = self._caller_id, extension = extension)
        logging.info("call to %s successfully removed", endpoint) #log completion
