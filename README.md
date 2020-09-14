# Generic USB Scanner to Python application

## Application
- Decode barcode, hash barcode tag and POST to localhost.

## Ubuntu 
* Create 10-local.rules at /etc/udev/rules.d
`ACTION=="add", SUBSYSTEMS=="usb", ENV{DEVTYPE}=="usb_device", ATTRS{idVendor}=="05e0", ATTRS{idProduct}=="1200", GROUP="plugdev", MODE="666"`

* Reload the usb sys conf
sudo udevadm control --reload
sudo udevadm trigger

* `pip install -r requirements.txt`
* `python general_usb_barcode.py`