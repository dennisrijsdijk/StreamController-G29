import os
import pyudev
from device import Device

class DeviceManager:

    def __init__(self):
        self.devices = {}
        self.changed = True

    def start(self):
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('input')
        self.init_device_list()

    def init_device_list(self):
        context = pyudev.Context()
        for udevice in context.list_devices(subsystem='input', ID_INPUT_JOYSTICK=1):
            self.update_device_list(udevice)

        self.changed = True

    def update_device_list(self, udevice):
        id = udevice.device_path
        device_node = udevice.device_node

        if not id or not device_node or not 'event' in udevice.get('DEVNAME'):
            return

        usb_id = str(udevice.get('ID_VENDOR_ID')) + ':' + str(udevice.get('ID_MODEL_ID'))
        if usb_id != '046d:c24f':
            return

        if id not in self.devices:
            self.devices[id] = Device(self, {})

        device = self.devices[id]

        device.set({
            'id': id,
            'vendor_id': udevice.get('ID_VENDOR_ID'),
            'product_id': udevice.get('ID_MODEL_ID'),
            'usb_id': usb_id,
            'dev_name': device_node,
            'dev_path': os.path.realpath(os.path.join(udevice.sys_path, 'device', 'device')),
            'name': bytes(udevice.get('ID_VENDOR_ENC') + ' ' + udevice.get('ID_MODEL_ENC'),
                          'utf-8').decode('unicode_escape'),
            'max_range': 900,
            })

    def first_device(self):
        if self.devices:
            return self.get_device(next(iter(self.devices)))
        return None

    def get_devices(self):
        return list(self.devices.values())

    def get_device(self, did):
        if did is None:
            return None
        if did in self.devices:
            return self.devices[did]
        return next((item for item in self.devices.values() if item.dev_name == did), None)

    def is_changed(self):
        changed = self.changed
        self.changed = False
        return changed
