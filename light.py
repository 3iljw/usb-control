from datetime import datetime
import threading

import usb
import wx


############################################

class LED(wx.Panel) :
    """SP motor setting and action tab page setting."""
    def __init__(self, parent, mainFrame) :
        """SP motor setting and action tab page setting inital."""
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
        self.event = threading.Event()
        read_thread = threading.Thread(target=self.read, args=epin)
        read_thread.start()

        ##########

        self.mainFrame = mainFrame

        wx.Panel.__init__(self, parent)
        sizer = wx.GridBagSizer(10, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        ##########
        sb1 = wx.StaticBox(self, label="CH1")
        sbs1 = wx.StaticBoxSizer(sb1)
        boxsizer1 = wx.GridBagSizer(6, 6)
        boxsizer1.Add(wx.StaticText(self, label  ="Current"), pos=(0,0),flag=wx.LEFT|wx.TOP)
        c1 = wx.TextCtrl(self, -1)
        boxsizer1.Add(self.c1, pos=(0,1), flag=wx.LEFT)
        sc1 = wx.Button(self, label="Set")
        sc1.Bind(wx.EVT_BUTTON, lambda event: self.setparams(event, epout=epout, snd_cmd=self.SetModeCurrent(0,int(c1.getValue()))))
        boxsizer1.Add(sc1, pos=(0,2), flag=wx.CENTRE)
        boxsizer1.Add(wx.StaticText(self, label  ="Voltage"), pos=(0,0),flag=wx.LEFT|wx.TOP)
        v1 = wx.TextCtrl(self, -1)
        boxsizer1.Add(self.v1, pos=(0,1), flag=wx.LEFT)
        sv1 = wx.Button(self, label="Set")
        sv1.Bind(wx.EVT_BUTTON, lambda event: self.setparams(event, epout=epout, snd_cmd=self.SetVoltage(0,int(v1.getValue()))))
        boxsizer1.Add(sv1, pos=(0,2), flag=wx.CENTRE)
        sbs1.Add(boxsizer1)
        sizer.Add(sbs1, pos=(0, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT)
        ##########
        ##########
        sb2 = wx.StaticBox(self, label="CH2")
        sbs2 = wx.StaticBoxSizer(sb2)
        boxsizer2 = wx.GridBagSizer(6, 6)
        boxsizer2.Add(wx.StaticText(self, label  ="Current"), pos=(0,0),flag=wx.LEFT|wx.TOP)
        c2 = wx.TextCtrl(self, -1)
        boxsizer2.Add(self.c2, pos=(0,1), flag=wx.LEFT)
        sc2 = wx.Button(self, label="Set")
        sc2.Bind(wx.EVT_BUTTON, lambda event: self.setparams(event, epout=epout, snd_cmd=self.SetModeCurrent(1,int(c2.getValue()))))
        boxsizer2.Add(sc2, pos=(0,2), flag=wx.CENTRE)
        boxsizer2.Add(wx.StaticText(self, label  ="Voltage"), pos=(0,0),flag=wx.LEFT|wx.TOP)
        v2 = wx.TextCtrl(self, -1)
        boxsizer2.Add(self.v2, pos=(0,1), flag=wx.LEFT)
        sv2 = wx.Button(self, label="Set")
        sv2.Bind(wx.EVT_BUTTON, lambda event: self.setparams(event, epout=epout, snd_cmd=self.SetVoltage(1,int(v2.getValue()))))
        boxsizer2.Add(sv2, pos=(0,2), flag=wx.CENTRE)
        sbs2.Add(boxsizer2)
        sizer.Add(sbs2, pos=(0, 1), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT)
        ##########
        ##########
        sb3 = wx.StaticBox(self, label="CH3")
        sbs3 = wx.StaticBoxSizer(sb3)
        boxsizer3 = wx.GridBagSizer(6, 6)
        boxsizer3.Add(wx.StaticText(self, label  ="Current"), pos=(0,0),flag=wx.LEFT|wx.TOP)
        c3 = wx.TextCtrl(self, -1)
        boxsizer3.Add(self.c3, pos=(0,1), flag=wx.LEFT)
        sc3 = wx.Button(self, label="Set")
        sc3.Bind(wx.EVT_BUTTON, lambda event: self.setparams(event, epout=epout, snd_cmd=self.SetModeCurrent(2,int(c3.getValue()))))
        boxsizer3.Add(sc3, pos=(0,2), flag=wx.CENTRE)
        boxsizer3.Add(wx.StaticText(self, label  ="Voltage"), pos=(0,0),flag=wx.LEFT|wx.TOP)
        v3 = wx.TextCtrl(self, -1)
        boxsizer3.Add(self.v3, pos=(0,1), flag=wx.LEFT)
        sv3 = wx.Button(self, label="Set")
        sv3.Bind(wx.EVT_BUTTON, lambda event: self.setparams(event, epout=epout, snd_cmd=self.SetVoltage(2,int(v3.getValue()))))
        boxsizer3.Add(sv3, pos=(0,2), flag=wx.CENTRE)
        sbs3.Add(boxsizer3)
        sizer.Add(sbs3, pos=(1, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT)
        ##########
        ##########
        sb4 = wx.StaticBox(self, label="CH4")
        sbs4 = wx.StaticBoxSizer(sb4)
        boxsizer4 = wx.GridBagSizer(6, 6)
        boxsizer4.Add(wx.StaticText(self, label  ="Current"), pos=(0,0),flag=wx.LEFT|wx.TOP)
        c4 = wx.TextCtrl(self, -1)
        boxsizer4.Add(self.c4, pos=(0,1), flag=wx.LEFT)
        sc4 = wx.Button(self, label="Set")
        sc4.Bind(wx.EVT_BUTTON, lambda event: self.setparams(event, epout=epout, snd_cmd=self.SetModeCurrent(3,int(c4.getValue()))))
        boxsizer4.Add(sc4, pos=(0,2), flag=wx.CENTRE)
        boxsizer4.Add(wx.StaticText(self, label  ="Voltage"), pos=(0,0),flag=wx.LEFT|wx.TOP)
        v4 = wx.TextCtrl(self, -1)
        boxsizer4.Add(self.v4, pos=(0,1), flag=wx.LEFT)
        sv4 = wx.Button(self, label="Set")
        sv4.Bind(wx.EVT_BUTTON, lambda event: self.setparams(event, epout=epout, snd_cmd=self.SetVoltage(3,int(v4.getValue()))))
        boxsizer4.Add(sv4, pos=(0,2), flag=wx.CENTRE)
        sbs4.Add(boxsizer4)
        sizer.Add(sbs4, pos=(1, 1), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT)
        ##########

        hbox.Add(sizer, 0, wx.ALL|wx.ALIGN_CENTER)
        vbox.Add(hbox, 1, wx.ALL|wx.ALIGN_CENTER, 5)
        self.SetSizerAndFit(vbox)
        vbox.Fit(self)

    def calc_value(self, value) :
        data = []
        data.append(value >> 8)
        data.append(value - (data[-1] << 8))

        return data

    def get_checksum(self, msg) :
        sum_ = bin(sum(msg))[2:]
        while len(sum_) > 8 : sum_ = sum_[-8:]
        sum_ = int(sum_,2)
        return sum_


    def SetCurrentLimit(self, channel, value) :
        data = self.calc_value(value)
        cmd = [0x88,0x55,0xaa,0x33,channel] + data
        cmd = cmd + [self.get_checksum(cmd)]
        return cmd

    def SetVoltageLimit(self, channel, value) :
        data = self.calc_value(value)
        cmd = [0x88,0x55,0xaa,0x36,channel] + data
        cmd = cmd + [self.get_checksum(cmd)]
        return cmd

    def SetModeCurrent(self, channel, value) :
        data = self.calc_value(value)
        mode = 0x00
        cmd = [0x89,0x55,0xaa,0x40,channel, mode] + data
        cmd = cmd + [self.get_checksum(cmd)]
        return cmd

    def SetVoltage(self, channel, value) :
        data = self.calc_value(value)
        cmd = [0x88,0x55,0xaa,0x43,channel] + data
        cmd = cmd + [self.get_checksum(cmd)]
        return cmd

    def read(self, epin) :
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
                if self.get_checksum(msg) == checksum and msg[1]==0xAA and msg[2]==0x55 :
                    print(msg+[checksum])
                    print(datetime.now())
                    self.event.set()
                else :
                    # print(''.join([chr(x) for x in list(lrec)]))
                    pass
            except usb.core.USBTimeoutError :
                pass

    def write(self, epout, snd_cmd) :
        while 1 :
            self.event.clear()
            itera = 0

            while not self.event.is_set() and itera < 3:
                print(datetime.now())
                itera += 1
                epout.write(snd_cmd)
                self.event.wait(1)
            if itera == 3 :
                print('timeout')