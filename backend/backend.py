from streamcontroller_plugin_tools import BackendBase

from DeviceManager import DeviceManager

from loguru import logger as log

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        self._ready = False
        self._device = None
        log.info("Launching G29 Control Backend")
        self._device_manager = DeviceManager()
        self._device_manager.start()
        devices = self._device_manager.get_devices()
        if len(devices) > 0:
            self._device = self._device_manager.first_device()
            if self._device and not self._device.check_permissions():
                log.error("Device permissions are not set correctly. Please install the 'Oversteer' program and reboot.")
                self._device = None
            else:
                self._ready = True

    #
    # STATE
    #
    def get_ready(self):
        return self._ready

    def get_rotation_range(self):
        if not self.get_ready():
            return None
        return self._device.get_range()

    def set_rotation_range(self, rotation):
        if not self.get_ready():
            return False
        return self._device.set_range(rotation)

    def get_autocenter_strength(self):
        if not self.get_ready():
            return None
        return self._device.get_autocenter()

    def set_autocenter_strength(self, strength):
        if not self.get_ready():
            return False
        return self._device.set_autocenter(strength)

backend = Backend()