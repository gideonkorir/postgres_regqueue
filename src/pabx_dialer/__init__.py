class Registration(object):
    """A registration object from sms we've received
    """

    def __init__(self, reg_id, phoneNumber):
        self._reg_id = reg_id
        self._phoneNumber = phoneNumber

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

    def __str__(self):
        return "{}, {}".format(self.reg_id, self.phone_number)


class RegistrationSource(object):
    """Represents a class that can fetch registrations
        
        Implementations provide a way to fetch pending registrations 
        and to mark them as processed

    """
    def __init__(self):
        pass

    def get_pending_registrations(self):
        """Abstract method to define contract for getting pending registrations
        """
        pass

    def mark_as_processed(self, registrations):
        """Abstract method to define contract for removing actioned registrations
        """
        pass

    def close(self):
        """clean up of the source if necessary
        """
        pass
