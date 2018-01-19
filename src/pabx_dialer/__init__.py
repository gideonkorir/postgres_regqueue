class Registration(object):
    """A registration object from sms we've received
    """

    def __init__(self, reg_id, phoneNumber, campaignid):
        self._reg_id = reg_id
        self._phoneNumber = phoneNumber
        self._campaignid = campaignid

    @property
    def reg_id(self):
        """The id of the registration, it's a 64-bit integer
        """
        return self._reg_id

    @property
    def phone_number(self):
        """The source phone #
        """
        return self._phoneNumber

    @property
    def campaign_id(self):
        """The campaign we are running
        """
        return self._campaignid

    def __str__(self):
        return "{}, {} for campaign {}".format(self.reg_id, self.phone_number, self._campaignid)

class CancellationToken:
    _cts = None

    def __init__(self, cts):
        self._cts = cts
    
    @property
    def is_cancelled(self):
        return self._cts.is_cancelled

class CancellationTokenSource(object):
    _cancelled = False

    def __init__(self):
        pass

    @property
    def is_cancelled(self):
        return self._cancelled

    @property
    def token(self):
        return CancellationToken(self)

    def cancel(self):
        self._cancelled = True



class RegistrationSource(object):
    """Represents a class that can fetch registrations
        
        Implementations provide a way to fetch pending registrations 
        and to mark them as processed

    """
    def __init__(self):
        pass

    def get_next_registration(self):
        """Abstract method to define contract for getting pending registrations
        """
        pass

    def mark_as_processed(self, registration):
        """Abstract method to define contract for removing actioned registrations
        """
        pass

    def close(self):
        """clean up of the source if necessary
        """
        pass
