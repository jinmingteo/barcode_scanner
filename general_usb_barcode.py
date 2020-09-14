import usb.core
import usb.util
import requests
from hash_helper import encrypt

# //return await axios.post('https://192.168.1.236:5000/detect_masked_face', formData);
#     return await axios.post('https://localhost:5000/detect_masked_face', formData);

url ='http://localhost:5000/scan_barcode'

def get_qr_value(lst):
    
    assert len(lst) == 8, 'Invalid data length (needs 8 bytes)'
    conv_table = {
        0:['', ''],
        4:['a', 'A'],
        5:['b', 'B'],
        6:['c', 'C'],
        7:['d', 'D'],
        8:['e', 'E'],
        9:['f', 'F'],
        10:['g', 'G'],
        11:['h', 'H'],
        12:['i', 'I'],
        13:['j', 'J'],
        14:['k', 'K'],
        15:['l', 'L'],
        16:['m', 'M'],
        17:['n', 'N'],
        18:['o', 'O'],
        19:['p', 'P'],
        20:['q', 'Q'],
        21:['r', 'R'],
        22:['s', 'S'],
        23:['t', 'T'],
        24:['u', 'U'],
        25:['v', 'V'],
        26:['w', 'W'],
        27:['x', 'X'],
        28:['y', 'Y'],
        29:['z', 'Z'],
        30:['1', '!'],
        31:['2', '@'],
        32:['3', '#'],
        33:['4', '$'],
        34:['5', '%'],
        35:['6', '^'],
        36:['7' ,'&'],
        37:['8', '*'],
        38:['9', '('],
        39:['0', ')'],
        40:['\n', '\n'],
        41:['\x1b', '\x1b'],
        42:['\b', '\b'],
        43:['\t', '\t'],
        44:[' ', ' '],
        45:['_', '_'],
        46:['=', '+'],
        47:['[', '{'],
        48:[']', '}'],
        49:['\\', '|'],
        50:['#', '~'],
        51:[';', ':'],
        52:["'", '"'],
        53:['`', '~'],
        54:[',', '<'],
        55:['.', '>'],
        56:['/', '?'],
        100:['\\', '|'],
        103:['=', '='],
        }

    # A 2 in first byte seems to indicate to shift the key. For example
    # a code for ';' but with 2 in first byte really means ':'.
    if lst[0] == 2:
        shift = 1
    else:
        shift = 0
        
    # The character to convert is in the third byte
    ch = lst[2]
    if ch not in conv_table:
        print ("Warning: data not in conversion table")
        return ''
    return conv_table[ch][shift]



def get_scanner(product_id):
    # Find our device using the VID (Vendor ID) and PID (Product ID)
    raw_scanner = usb.core.find(idVendor=0x05e0, idProduct=product_id)
    #raw_scanner = usb.core.find(idVendor=05e0, idProduct=1200)
    return raw_scanner

def remove_form_kernel(raw_scanner):
    # Disconnect it from kernel
    needs_reattach = False
    if raw_scanner.is_kernel_driver_active(0):
        needs_reattach = True
        
        raw_scanner.detach_kernel_driver(0)
        print ("Detached USB device from kernel driver")
    return needs_reattach


def scanner_config(raw_scanner):
    raw_scanner.set_configuration()
    # get an endpoint instance
    cfg = raw_scanner.get_active_configuration()
    intf = cfg[(0,0)]

    scanner = usb.util.find_descriptor(
        intf,
        # match the first IN endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)
    return scanner



raw_scanner_obj = get_scanner(0x1200)
if raw_scanner_obj == None:
    raise Exception("Please insert the USB barcode scanner")
    
else:
    needs_reattach = remove_form_kernel(raw_scanner_obj)
    scanner = scanner_config(raw_scanner_obj)


def main():
    line = ''
    while True:
        try:
            data = scanner.read(1000, 500)
            ch = get_qr_value(data)
            line += ch
        except Exception as e:
            if len(line) > 0:
                resp = requests.post(url, data = {'hash': encrypt(line)})
                print (resp.text)
                print (line)
                
                line = ''

if __name__ == '__main__':   
    main()