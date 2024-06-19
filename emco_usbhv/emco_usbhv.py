import hid

# Vendor ID and Product ID of the device (USB20N)
VENDOR_ID = 0x03eb
# PRODUCT_ID = 0x201d

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
    # create a function which will list all available device's IDs correspoding to the vendor ID
    @staticmethod
    def list_devices():
        devices = hid.enumerate()
        return [(device['vendor_id'], device['product_id']) for device in devices if device['vendor_id'] == VENDOR_ID]
        
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
        v = voltage * 2
        voltage_high_byte = (v >> 8) & 0xFF
        voltage_low_byte = v & 0xFF
        command = [0x01, voltage_low_byte, voltage_high_byte, 0x00, 0x00, 0x0f, 0xff, 0x09]
        self.write_data(command)
        response = self.read_data(8)
        print(f'Set voltage to {voltage} V (binary: 0x{v:04x}), response: {response}')
        

    def enable_output(self):
        command = [0x02, 0x80, 0xcc, 0x00, 0x00, 0x0f, 0xff, 0x09]
        self.write_data(command)
        response = self.read_data(8)
        print(f'Enabled output, response: {response}')

    def disable_output(self):
        command = [0x02, 0x00, 0xcc, 0x00, 0x00, 0x0f, 0xff, 0x09]
        self.write_data(command)
        response = self.read_data(8)
        print(f'Disabled output, response: {response}')

    def get_status(self):
        command = [0x03, 0x00, 0xcc, 0x00, 0x00, 0x0f, 0xff, 0x09]
        self.write_data(command)
        response = self.read_data(8)
        status = {}
        print(f'Status response: {response}')
        status['enabled'] = response[0] == 0x80
        status['set_voltage'] = (response[2] << 8) | response[1]
        status['voltage_monitor1'] = (response[4] << 8) | response[3]
        status['voltage_monitor2'] = (response[6] << 8) | response[5]
        return status
    
    # create properties for the power supply
    @property
    def voltage(self):
        return self._set_voltage
    
    @voltage.setter
    def voltage(self, value):
        self._set_voltage = value
        voltage_high_byte = (value >> 8) & 0xFF
        voltage_low_byte = value & 0xFF
        command = [0x01, voltage_low_byte, voltage_high_byte, 0x00, 0x00, 0x0f, 0xff, 0x09]
        self.write_data(command)

if 0:

    # Open the device
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)

    # Print device info
    print(f'Manufacturer: {device.get_manufacturer_string()}')
    print(f'Product: {device.get_product_string()}')
    print(f'Serial Number: {device.get_serial_number_string()}')

    # Command to set voltage (example, replace with actual command)
    # Assuming the command to set voltage is [0x01, 0x02, voltage_high_byte, voltage_low_byte]
    voltage = 500  # 500V, example value
    voltage_high_byte = (voltage >> 8) & 0xFF
    voltage_low_byte = voltage & 0xFF

    # set voltage
    command = [0x00, 0x01, 0xff, 0x03, 0, 0, 0x0f, 0xff, 0x09]

    # Send command to the device
    write_data(device, command)

    # Read response from the device
    response = read_data(device, 8)  # Adjust length as needed
    print('Response:', response)

    # reset command
    command = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0xff, 0x09]

    # enable output
    command = [0x00, 0x02, 0x80, 0xcc, 0x00, 0x00, 0x0f, 0xff, 0x09]
    # disable output
    #command = [0x00, 0x02, 0x00, 0xcc, 0x00, 0x00, 0x0f, 0xff, 0x09]



    # Send command to the device
    write_data(device, command)

    # Read response from the device
    response = read_data(device, 8)  # Adjust length as needed
    print('Response:', response)



    # request status
    command = [0x00, 0x03, 0x00, 0xcc, 0x00, 0x00, 0x0f, 0xff, 0x09]

    # Send command to the device
    write_data(device, command)

    # Read response from the device
    response = read_data(device, 8)  # Adjust length as needed
    print('Response:', response)

    # 500 V requested
    # 496 V measured - enabled
    # 80 03 ff 03 f8 03 f8 09

    # some time after disabling the output voltage
    # 00 03 ff 03 b9 02 83 09

    # long time after disabling the output voltage
    # 00 03 f8 01 7f 0f ff 09

    # response contains actual set voltage
    # and measured voltage
    # first byte is 80 if enabled
    # 2B - set voltage: big endian
    # 2B - measured voltage 1: big endian
    # 2B - measured voltage 2: big endian


    # Close the device
    device.close()
