import threading
from datetime import datetime

import usb

event = threading.Event()
itera = 0


def calc_value(value) :
    data = []
    data.append(value >> 8)
    data.append(value - (data[-1] << 8))

    return data

def get_checksum(msg) :
    sum_ = bin(sum(msg))[2:]
    while len(sum_) > 8 : sum_ = sum_[-8:]
    sum_ = int(sum_,2)
    return sum_


def SetCurrentLimit(channel, value) :
    data = calc_value(value)
    cmd = [0x88,0x55,0xaa,0x33,channel] + data
    cmd = cmd + [get_checksum(cmd)]
    return cmd

def SetVoltageLimit(channel, value) :
    data = calc_value(value)
    cmd = [0x88,0x55,0xaa,0x36,channel] + data
    cmd = cmd + [get_checksum(cmd)]
    return cmd

def SetModeCurrent(channel, value) :
    data = calc_value(value)
    mode = 0x00
    cmd = [0x89,0x55,0xaa,0x40,channel, mode] + data
    cmd = cmd + [get_checksum(cmd)]
    return cmd

def SetVoltage(channel, value) :
    data = calc_value(value)
    cmd = [0x88,0x55,0xaa,0x43,channel] + data
    cmd = cmd + [get_checksum(cmd)]
    return cmd

def read(epin) :
    print('recv ... ')
    t2 = threading.current_thread()
    while t2.open :
        try :
            rec = epin.read(64)
            lrec = list(rec)
            print(lrec)
            LEN = lrec[0]-0x80
            msg = lrec[:LEN-1]
            checksum = lrec[LEN-1]
            if get_checksum(msg) == checksum and msg[1]==0xAA and msg[2]==0x55 :
                print(msg+[checksum])
                print(datetime.now())
                event.set()
            else :
                # print(''.join([chr(x) for x in list(lrec)]))
                pass
        except usb.core.USBTimeoutError :
            pass

def write(epout) :
    while 1 :
        event.clear()
        cmd = str(input('input(type \'q\' to quit) : '))
        if cmd == 'q' : break
        cmd = cmd.split(',')
        try : cmd = [int(x) for x in cmd]
        except ValueError : continue
        itera = 0
        cmd_data = [0x80+len(cmd)+4, 0x55, 0xAA] + cmd
        cmdchecksum = get_checksum(cmd_data)
        snd_cmd = cmd_data+[cmdchecksum]
        print(snd_cmd)
        while not event.is_set() and itera < 3:
            print(datetime.now())
            itera += 1
            epout.write(snd_cmd)
            event.wait(1)
        if itera == 3 :
            print('timeout')

if __name__ == '__main__':
    # mydev = usb.core.find(idVendor=0x8888, idProduct=0xBBBB, find_all=True)
    mydev = usb.core.find(idVendor=0x8888, idProduct=0x7000)

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

    t1 = threading.Thread(target=read, args=(epin,))
    t1.open = True
    t1.start()

    t2 = threading.Thread(target=write, args=(epout,))
    t2.start()

    t2.join()
    t1.open = False 
    t1.join()

