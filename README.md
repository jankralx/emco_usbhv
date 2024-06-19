# EMCO USB_HV control module in Python with HID API

This is a Python module to control the EMCO USB_HV power module via the HID API. The module is based on the reverse engineering of the USB protocol used by the EMCO USBhv Series control software. It was tested with USB20N power module.

## Installation

TBD

On Linux remember to set correct permissions for the USB device. You can do it by creating a udev rule. Create a file `/etc/udev/rules.d/99-emco-usbhv.rules` with the following content:
```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="03eb", ATTR{idProduct}=="201d", MODE="0666"
```
or simply run the following command:
```bash
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="03eb", ATTR{idProduct}=="201d", MODE="0666"' | sudo tee /etc/udev/rules.d/99-emco-usbhv.rules
```
Then reload the udev rules:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Usage

```python
import emco_usbhv

# TBD ...

```

## GUI Application

The module also includes a simple GUI application to control the EMCO USB_HV power module. The application is based on the `tkinter` library.

Run the application with the following command:
```bash
python -m emco_usbhv
