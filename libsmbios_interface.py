import ctypes

class LibsmbiosInterface:
    def __init__(self):
        # Load the libsmbios library
        self.lib = ctypes.cdll.LoadLibrary('/usr/lib64/libsmbios_c.so.2')

    def read_thermal_behavior(self):
        # Call the libsmbios function to read thermal behavior
        self.lib.smbios_thermal_behavior_read.restype = ctypes.c_char_p
        result = self.lib.smbios_thermal_behavior_read()
        return result.decode()

    def set_thermal_behavior(self, behavior):
        # Call the libsmbios function to set thermal behavior
        self.lib.smbios_thermal_behavior_set.argtypes = [ctypes.c_char_p]
        self.lib.smbios_thermal_behavior_set(behavior.encode())

    def read_battery_behavior(self):
        # Call the libsmbios function to read battery behavior
        self.lib.smbios_battery_behavior_read.restype = ctypes.c_char_p
        self.lib.dell_smi_read_battery_mode_setting()
        result = self.lib.smbios_battery_behavior_read()
        return result.decode()

    def set_battery_behavior(self, behavior, param1=None, param2=None):
        # Call the libsmbios function to set battery behavior
        self.lib.smbios_battery_behavior_set.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.lib.smbios_battery_behavior_set(behavior.encode(), param1.encode() if param1 else None, param2.encode() if param2 else None)
