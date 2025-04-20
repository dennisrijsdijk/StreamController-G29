from evdev import ecodes
import grp
import os
import pwd

class Device:

    def __init__(self, device_manager, data):
        self.device_manager = device_manager
        self.input_device = None
        self.id = None
        self.vendor_id = None
        self.product_id = None
        self.usb_id = None
        self.dev_path = None
        self.dev_name = None
        self.name = None
        self.ready = True
        self.max_range = None

        self.set(data)

    def set(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def close(self):
        if self.input_device is not None:
            self.input_device.close()
            self.input_device = None

    def disable(self):
        self.dev_name = None
        self.ready = False
        self.close()

    def enable(self):
        self.ready = True

    def is_ready(self):
        return self.ready

    def get_id(self):
        return self.id

    def device_file(self, filename):
        return os.path.join(self.dev_path, filename)

    def checked_device_file(self, filename):
        path = self.device_file(filename)
        if not os.access(path, os.F_OK | os.R_OK | os.W_OK):
            return False
        return path

    def check_file_permissions(self, filename):
        if filename is None:
            return True
        path = self.device_file(filename)
        if not os.access(path, os.F_OK):
            return True
        if os.access(path, os.R_OK | os.W_OK):
            return True
        return False

    def get_range(self):
        path = self.checked_device_file("range")
        if not path:
            return None
        with open(path, "r") as file:
            data = file.read()
        wrange = data.strip()
        return int(wrange)

    def set_range(self, wrange):
        path = self.checked_device_file("range")
        if not path:
            return False
        wrange = str(wrange)
        with open(path, "w") as file:
            file.write(wrange)
        return True

    def get_autocenter(self):
        path = self.checked_device_file("autocenter")
        if not path:
            capabilities = self.get_capabilities()
            if ecodes.EV_FF in capabilities and ecodes.FF_AUTOCENTER in capabilities[ecodes.EV_FF]:
                return 0
            else:
                return None
        with open(path, "r") as file:
            data = file.read()
        autocenter = data.strip()
        return int(round((int(autocenter) * 100) / 65535))

    def set_autocenter(self, autocenter):
        if autocenter > 100:
            autocenter = 100
        autocenter = str(int(autocenter / 100.0 * 65535))
        path = self.checked_device_file("autocenter")
        if path:
            with open(path, "w") as file:
                file.write(autocenter)
        else:
            input_device = self.get_input_device()
            input_device.write(ecodes.EV_FF, ecodes.FF_AUTOCENTER, int(autocenter))
        return True

    def check_permissions(self):
        if not os.access(self.dev_path, os.F_OK | os.R_OK | os.X_OK):
            return False
        if not self.check_file_permissions('range'):
            return False
        if not self.check_file_permissions('autocenter'):
            return False
        return True

    def get_capabilities(self):
        return self.get_input_device().capabilities()
