import hid

# Captured commands and responses from the device
# reset
# 00 00 00 00 00 0f ff 09
# get status
# 03 00 cc 00 00 0f ff 09
# set voltage (500 V)
# 01 xx yy 00 00 0f ff 09
# where xx is the low byte and yy is the high byte of the voltage variable
# voltage variable is twice the desired voltage
# e.g. for 500 V, xx = 0xff, yy = 0x03 (not exactly twice, seems there is a conversion table of function)
# 01 ff 03 00 00 0f ff 09
# enable output
# 02 80 cc 00 00 0f ff 09
# disable output
# 02 00 cc 00 00 0f ff 09

# response on get status command
# - contains actual set voltage and measured voltages
# 1B - status (0x80 if enabled, 0x00 if disabled)
# 2B - set voltage: big endian (opposite order of the set voltage command)
# 2B - measured voltage 1: big endian
# 2B - measured voltage 2: big endian

# this driver does not have any calibration curve for the voltage
# therefore, I would recommend to calibrate your module with a multimeter

class EMCO_USBhv:
    # Vendor ID and Product ID of the device (USB20N)
    C_VENDOR_ID = 0x03eb
    # C_PRODUCT_ID = 0x201d

    # create a function which will list all available device's IDs correspoding to the vendor ID
    @staticmethod
    def list_devices():
        devices = hid.enumerate()
        return [(device['vendor_id'], device['product_id']) for device in devices if device['vendor_id'] == EMCO_USBhv.C_VENDOR_ID]
    
    # constructor
    def __init__(self, vendor_id=None, product_id=None):
        self.vendor_id = vendor_id
        self.product_id = product_id

        # if vendor_id and product_id are not provided, find the device
        if vendor_id is None or product_id is None:
            devices = EMCO_USBhv.list_devices()
            if len(devices) == 0:
                raise Exception('No EMCO USBhv device found')
            if len(devices) > 1:
                raise Exception('Multiple EMCO USBhv devices found, specify the vendor_id and product_id')
            self.vendor_id, self.product_id = devices[0]
        
        self.device = hid.device()
        self.device.open(self.vendor_id, self.product_id)

    # destructor
    def __del__(self):
        self.device.close()
    
    def write_data(self, data):
        # add 0x00 to the beginning of the data
        data = [0x00] + data
        self.device.write(data)

    def read_data(self, length):
        return self.device.read(length)
    
    def set_voltage(self, voltage):
        if voltage < 0 or voltage >= 2048:
            raise Exception('Voltage must be between 0 and 2000 V')
        
        v = voltage * 2
        voltage_high_byte = (v >> 8) & 0xFF
        voltage_low_byte = v & 0xFF
        command = [0x01, voltage_low_byte, voltage_high_byte, 0x00, 0x00, 0x0f, 0xff, 0x09]
        self.write_data(command)
        response = self.read_data(8)
        #print(f'Set voltage to {voltage} V (binary: 0x{v:04x}), response: {response}')
        

    def enable(self):
        command = [0x02, 0x80, 0xcc, 0x00, 0x00, 0x0f, 0xff, 0x09]
        self.write_data(command)
        response = self.read_data(8)
        #print(f'Enabled output, response: {response}')

    def disable(self):
        command = [0x02, 0x00, 0xcc, 0x00, 0x00, 0x0f, 0xff, 0x09]
        self.write_data(command)
        response = self.read_data(8)
        #print(f'Disabled output, response: {response}')

    def status(self):
        command = [0x03, 0x00, 0xcc, 0x00, 0x00, 0x0f, 0xff, 0x09]
        self.write_data(command)
        response = self.read_data(8)
        status = {}
        #print(f'Status response: {response}')
        status['enabled'] = response[0] == 0x80
        status['set_voltage'] = ((response[1] << 8) | response[2]) / 2.0
        status['voltage_monitor1'] = ((response[3] << 8) | response[4]) / 2.0
        status['voltage_monitor2'] = ((response[5] << 8) | response[6]) / 2.0
        return status

    # set voltage directly by calling the object with the voltage value
    def __call__(self, voltage):
        self.set_voltage(voltage)
 

if __name__ == '__main__':
    import time

    # create an object of the class
    hv = EMCO_USBhv()

    # set the voltage to 500 V
    hv.set_voltage(500)

    # enable the output
    hv.enable()

    # get the status
    time.sleep(0.3)
    print(f'Status after setting 500 V and enabled: {hv.status()}')

    # disable the output
    hv.disable()

    # get the status
    time.sleep(0.3)
    print(f'Status after disabling: {hv.status()}')

    # set the voltage to 1000 V
    hv(1000)

    # enable the output
    hv.enable()

    # get the status
    time.sleep(0.3)
    print(f'Status after setting 1000 V and enabled: {hv.status()}')

    # disable the output
    hv.disable()

    # get the status
    time.sleep(0.3)
    print(f'Status after disabling: {hv.status()}')