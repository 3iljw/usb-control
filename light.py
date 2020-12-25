from datetime import datetime
import threading

import usb
import wx


############################################

class LED(wx.Panel) :
    """SP light setting and action tab page setting."""
    def __init__(self, parent, mainFrame) :
        """SP light setting and action tab page setting inital."""
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
        self.epout = usb.util.find_descriptor(
            inf,
            custom_match = lambda e : usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )
        self.epin = usb.util.find_descriptor(
            inf,
            custom_match = lambda e : usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )
        self.event = threading.Event()
        self.read_thread = threading.Thread(target=self.read)
        self.read_thread.open = True
        self.read_thread.start()

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
        boxsizer1.Add(wx.StaticText(self, label="Current"), pos=(0,0),flag=wx.LEFT|wx.TOP, border=5)
        c1 = wx.TextCtrl(self, -1)
        boxsizer1.Add(c1, pos=(0,1), flag=wx.LEFT, border=5)
        sc1 = wx.Button(self, label="Set")
        sc1.Bind(wx.EVT_BUTTON, lambda event: self.write(event, snd_cmd=self.SetModeCurrent(0,int(c1.GetValue()))))
        boxsizer1.Add(sc1, pos=(0,2), flag=wx.CENTRE, border=5)
        boxsizer1.Add(wx.StaticText(self, label="Voltage"), pos=(1,0),flag=wx.LEFT|wx.TOP, border=5)
        v1 = wx.TextCtrl(self, -1)
        boxsizer1.Add(v1, pos=(1,1), flag=wx.LEFT, border=5)
        sv1 = wx.Button(self, label="Set")
        sv1.Bind(wx.EVT_BUTTON, lambda event: self.write(event, snd_cmd=self.SetVoltage(0,int(v1.GetValue()))))
        boxsizer1.Add(sv1, pos=(1,2), flag=wx.CENTRE, border=5)
        sbs1.Add(boxsizer1, border=5)
        sizer.Add(sbs1, pos=(0, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)
        ##########
        ##########
        sb2 = wx.StaticBox(self, label="CH2")
        sbs2 = wx.StaticBoxSizer(sb2)
        boxsizer2 = wx.GridBagSizer(6, 6)
        boxsizer2.Add(wx.StaticText(self, label="Current"), pos=(0,0),flag=wx.LEFT|wx.TOP, border=5)
        c2 = wx.TextCtrl(self, -1)
        boxsizer2.Add(c2, pos=(0,1), flag=wx.LEFT, border=5)
        sc2 = wx.Button(self, label="Set")
        sc2.Bind(wx.EVT_BUTTON, lambda event: self.write(event, snd_cmd=self.SetModeCurrent(1,int(c2.GetValue()))))
        boxsizer2.Add(sc2, pos=(0,2), flag=wx.CENTRE, border=5)
        boxsizer2.Add(wx.StaticText(self, label="Voltage"), pos=(1,0),flag=wx.LEFT|wx.TOP, border=5)
        v2 = wx.TextCtrl(self, -1)
        boxsizer2.Add(v2, pos=(1,1), flag=wx.LEFT, border=5)
        sv2 = wx.Button(self, label="Set")
        sv2.Bind(wx.EVT_BUTTON, lambda event: self.write(event, snd_cmd=self.SetVoltage(1,int(v2.GetValue()))))
        boxsizer2.Add(sv2, pos=(1,2), flag=wx.CENTRE, border=5)
        sbs2.Add(boxsizer2, border=5)
        sizer.Add(sbs2, pos=(0, 1), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)
        ##########
        ##########
        sb3 = wx.StaticBox(self, label="CH3")
        sbs3 = wx.StaticBoxSizer(sb3)
        boxsizer3 = wx.GridBagSizer(6, 6)
        boxsizer3.Add(wx.StaticText(self, label="Current"), pos=(0,0),flag=wx.LEFT|wx.TOP, border=5)
        c3 = wx.TextCtrl(self, -1)
        boxsizer3.Add(c3, pos=(0,1), flag=wx.LEFT, border=5)
        sc3 = wx.Button(self, label="Set")
        sc3.Bind(wx.EVT_BUTTON, lambda event: self.write(event, snd_cmd=self.SetModeCurrent(2,int(c3.GetValue()))))
        boxsizer3.Add(sc3, pos=(0,2), flag=wx.CENTRE, border=5)
        boxsizer3.Add(wx.StaticText(self, label="Voltage"), pos=(1,0),flag=wx.LEFT|wx.TOP, border=5)
        v3 = wx.TextCtrl(self, -1)
        boxsizer3.Add(v3, pos=(1,1), flag=wx.LEFT, border=5)
        sv3 = wx.Button(self, label="Set")
        sv3.Bind(wx.EVT_BUTTON, lambda event: self.write(event, snd_cmd=self.SetVoltage(2,int(v3.GetValue()))))
        boxsizer3.Add(sv3, pos=(1,2), flag=wx.CENTRE, border=5)
        sbs3.Add(boxsizer3, border=5)
        sizer.Add(sbs3, pos=(1, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)
        ##########
        ##########
        sb4 = wx.StaticBox(self, label="CH4")
        sbs4 = wx.StaticBoxSizer(sb4)
        boxsizer4 = wx.GridBagSizer(6, 6)
        boxsizer4.Add(wx.StaticText(self, label="Current"), pos=(0,0),flag=wx.LEFT|wx.TOP, border=5)
        c4 = wx.TextCtrl(self, -1)
        boxsizer4.Add(c4, pos=(0,1), flag=wx.LEFT, border=5)
        sc4 = wx.Button(self, label="Set")
        sc4.Bind(wx.EVT_BUTTON, lambda event: self.write(event, snd_cmd=self.SetModeCurrent(3,int(c4.GetValue()))))
        boxsizer4.Add(sc4, pos=(0,2), flag=wx.CENTRE, border=5)
        boxsizer4.Add(wx.StaticText(self, label="Voltage"), pos=(1,0),flag=wx.LEFT|wx.TOP, border=5)
        v4 = wx.TextCtrl(self, -1)
        boxsizer4.Add(v4, pos=(1,1), flag=wx.LEFT, border=5)
        sv4 = wx.Button(self, label="Set")
        sv4.Bind(wx.EVT_BUTTON, lambda event: self.write(event, snd_cmd=self.SetVoltage(3,int(v4.GetValue()))))
        boxsizer4.Add(sv4, pos=(1,2), flag=wx.CENTRE, border=5)
        sbs4.Add(boxsizer4, border=5)
        sizer.Add(sbs4, pos=(1, 1), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)
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

    def read(self) :
        # print('recv ... ')
        while self.read_thread.open :
            try :
                rec = self.epin.read(64)
                lrec = list(rec)
                LEN = lrec[0]-0x80
                msg = lrec[:LEN-1]
                checksum = lrec[LEN-1]
                if self.get_checksum(msg) == checksum and msg[1]==0xAA and msg[2]==0x55 :
                    # print(msg+[checksum])
                    self.event.set()
                else :
                    # print(''.join([chr(x) for x in list(lrec)]))
                    pass
            except usb.core.USBTimeoutError :
                pass

    def write(self, _event, snd_cmd) :
        self.event.clear()
        itera = 0
        # print('send',snd_cmd)

        while not self.event.is_set() and itera < 3:
            itera += 1
            self.epout.write(snd_cmd)
            self.event.wait(0.3)
        if itera == 3 :
            print('timeout')