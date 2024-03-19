""" Photon counter class unit"""

__version__ = '19.03.2024'
__author__ = 'Serhiy Kobyakov'


from arduino_device import ArduinoDevice


class PhotonCounter(ArduinoDevice):
    """ New Arduino device class template """
    # define the device name:
    # this is the string with which the device responds to b'?' query
    _device_name = "PhotonCounter"

    # other device-specific variables go here:

    def __init__(self, comport):
        """ Initialization of PhotonCounter"""
        # repeat assigning class variables
        # so they are visible in self.__dict__:
        self._device_name = self._device_name

        # start serial communication with the device
        # this is the place for the line!
        super().__init__(comport)

        # do some default device-specific init actions here:

    def __del__(self):
        # do some default device-specific finalization actions here:

        # this is the place for the line!
        super().__del__()

    def set_measuring_interval(self, meas_int: float) -> float:
        """set measuring interval (exposition)
        and return the actual interval after setting"""
        return float(self.send_and_get_answer(f"e{meas_int}"))

    def get_cps(self) -> float:
        """get actual reading (counts per second)"""
        return float(self.send_and_get_answer('r'))
