import threading
import time

import usb

def get_checksum(msg) :
    cmd_len = len(msg)+2
    # cmd_data = list(bytearray(msg.encode('ascii')))
    sum_ = cmd_len+sum(msg)
    sum_ = bin(sum_)[2:]
    sum_ = ''.join(['0' if s=='1' else '1' for s in sum_])
    sum_ = hex(int(sum_,2)+1)[2:]
    if len(sum_) > 2 : sum_ = sum_[-2:]
    while len(sum_) < 2 : sum_ = '0' + sum_
    sum_ = int(sum_,16)

    return sum_


def read(epin) :
    print('recv ... ')
    while 1 :
        try :
            rec = epin.read(64)
            lrec = list(rec)
            print(lrec)
            LEN = lrec[0]
            msg = lrec[1:LEN-1]
            checksum = lrec[LEN-1]
            if get_checksum(msg) == checksum :
                print(''.join([chr(x) for x in list(msg)]))
        except usb.core.USBTimeoutError :
            pass
def write(dev, command) :
    dev.write(command)

# mydev = usb.core.find(idVendor=0x8888, idProduct=0xBBBB, find_all=True)
mydev = usb.core.find(idVendor=0x8888, idProduct=0xBBBB)

if not mydev : raise ValueError('Device not found')

d = mydev
# dlist = []
# for d in mydev : dlist.append(d)
# for d in dlist : 
# reatach = False
if d.is_kernel_driver_active(0) :
    # reatach = True
    d.detach_kernel_driver(0)
d.set_configuration()
cfg = d.get_active_configuration()
inf = cfg[(0,0)]
epout = usb.util.find_descriptor(
    inf,
    custom_match = lambda e : usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)
epin = usb.util.find_descriptor(
    inf,
    custom_match = lambda e : usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

# readthreading = []
# for d in dlist :
#     readthreading.append(threading.Thread(target=read, args=d))
#     readthreading[-1].start()
t1 = threading.Thread(target=read, args=(epin,))
t1.start()

assert epout is not None
time.sleep(2)
print('send msg')

cmd = 'GETCHO'
cmd_data = list(bytearray(cmd.encode('ascii')))
cmdchecksum = get_checksum(cmd_data)
snd_cmd = [len(cmd)+2]+cmd_data+[cmdchecksum]

print(snd_cmd)

epout.write(snd_cmd)