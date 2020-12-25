import threading

import usb
import wx


############################################

class Motor(wx.Panel) :
    """SP motor setting and action tab page setting."""
    def __init__(self, parent, mainFrame) :
        """SP motor setting and action tab page setting inital."""        
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
        self.epout = usb.util.find_descriptor(
            inf,
            custom_match = lambda e : usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )
        self.epin = usb.util.find_descriptor(
            inf,
            custom_match = lambda e : usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )
        self.send_msg = None 
        self.event = threading.Event()
        self.read_thread = threading.Thread(target=self.read)
        self.read_thread.open = True
        self.read_thread.start()

        ##########

        self.mainFrame = mainFrame

        wx.Panel.__init__(self, parent)
        sizer = wx.GridBagSizer(10, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # par_data = [[None]*6 for x in range(4)]
        get_par = wx.Button(self, label = 'Read')
        get_par.Bind(wx.EVT_BUTTON, lambda event : self.get_par_fun())
        sizer.Add(get_par, pos=(1,0))

        boxsizer = wx.GridBagSizer(6, 6)
        # Create table information
        tablelbl = []
        # Create parameter setting bottom
        self.par_set = []
        tablelbl_data = ["","ON/OFF","Freq","Duty","Current"]
        for i in range(5) :
            if i != 0 :
                # print(i, pdata[i-1])
                self.par_set.append(wx.Button(self, label = f'Set {tablelbl_data[i]}'))
                boxsizer.Add(self.par_set[-1], pos=(7,i), flag=wx.ALIGN_CENTRE, border=5)
            tablelbl.append(wx.StaticText(self, label = tablelbl_data[i]))
            boxsizer.Add(tablelbl[i], pos=(0,i), flag=wx.ALIGN_CENTRE, border=5)

        self.par_set[0].Bind(wx.EVT_BUTTON, lambda event : self.setpa(params='CHO'))
        self.par_set[1].Bind(wx.EVT_BUTTON, lambda event : self.setpa(params='CHF'))
        self.par_set[2].Bind(wx.EVT_BUTTON, lambda event : self.setpa(params='CHD'))
        self.par_set[3].Bind(wx.EVT_BUTTON, lambda event : self.setpa(params='CHC'))

        # Create motor name label
        mtrlbl = []
        # Create channel setting bottom 
        self.ch_set = []
        # Create on/off control checkbox
        self.cho = []
        for i in range(6) :
            mtrlbl.append(wx.StaticText(self, label = f'CH{i+1}'))
            self.ch_set.append(wx.Button(self, label = f'Set CH{i+1}'))
            self.cho.append(wx.CheckBox(self))
            self.cho[-1].SetValue(1)
            boxsizer.Add(mtrlbl[i], pos=(i+1,0), flag=wx.ALIGN_CENTRE, border=5)
            boxsizer.Add(self.ch_set[i], pos=(i+1,5), flag=wx.ALIGN_CENTRE, border=5)
            boxsizer.Add(self.cho[i], pos=(i+1,1), flag=wx.ALIGN_CENTRE, border=5)

        self.ch_set[0].Bind(wx.EVT_BUTTON, lambda event : self.setch(channel=1))
        self.ch_set[1].Bind(wx.EVT_BUTTON, lambda event : self.setch(channel=2))
        self.ch_set[2].Bind(wx.EVT_BUTTON, lambda event : self.setch(channel=3))
        self.ch_set[3].Bind(wx.EVT_BUTTON, lambda event : self.setch(channel=4))
        self.ch_set[4].Bind(wx.EVT_BUTTON, lambda event : self.setch(channel=5))
        self.ch_set[5].Bind(wx.EVT_BUTTON, lambda event : self.setch(channel=6))

        # Create table text ctrl
        self.textctrl = []
        for i in range(6) :
            for j in range(3) :
                self.textctrl.append(wx.TextCtrl(self, size=(80, 23)))
                boxsizer.Add(self.textctrl[i*3+j], pos=(1+i,2+j), flag=wx.ALIGN_CENTRE, border=5)
        setall = wx.Button(self, label='Set All')
        setall.Bind(wx.EVT_BUTTON, lambda event : self.set_par_fun())
        boxsizer.Add(setall, pos=(7,5), flag=wx.EXPAND|wx.TOP|wx.CENTRE)
        sizer.Add(boxsizer, pos=(0, 1), span=(8, 2), flag=wx.EXPAND|wx.TOP|wx.CENTRE)

        sizer.Add(wx.StaticText(self, label='Repeat'), pos=(1, 3), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT)
        cnt = wx.TextCtrl(self, value='0', size=(50, 23))
        sizer.Add(cnt, pos=(1,4), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT)
        run = wx.Button(self, label = 'RUN')
        run.Bind(wx.EVT_BUTTON, lambda event : self.write(cmd='RUN'))
        sizer.Add(run, pos=(2,4))
        pause = wx.Button(self, label = 'PAUSE')
        pause.Bind(wx.EVT_BUTTON, lambda event : self.write(cmd='PAUSE'))
        sizer.Add(pause, pos=(3,4))
        stop = wx.Button(self, label = 'STOP')
        stop.Bind(wx.EVT_BUTTON, lambda event : self.write(cmd='STOP'))
        sizer.Add(stop, pos=(4,4))

        ##########
        sb_coil = wx.StaticBox(self, label='Coil')
        sbs_coil = wx.StaticBoxSizer(sb_coil)
        coil_boxsizer = wx.GridBagSizer(5,5)

        coil_list = ['Mode','Freq','Duty','Current']
        coil_textctrl = []
        for i in range(4) :
            coil_boxsizer.Add(wx.StaticText(self, label=coil_list[i]), pos=(i,0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)
            coil_textctrl.append(wx.TextCtrl(self, size=(80, 23)))
            coil_boxsizer.Add(coil_textctrl[-1], pos=(i,1), border=5)

        set_coil = wx.Button(self, label='Set')
        # set_coil.Bind(wx.EVT_BUTTON, lambda event : self.write(cmd=None))
        coil_boxsizer.Add(set_coil, pos=(3,2), border=5)
        coil_boxsizer.Add(wx.StaticText(self, label='Repeat'), pos=(5,0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)
        coil_cnt = wx.TextCtrl(self)
        coil_boxsizer.Add(coil_cnt, pos=(5,1), border=5)

        coil_run = wx.Button(self, label = 'RUN')
        coil_boxsizer.Add(coil_run, pos=(6,1), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)
        coil_stop = wx.Button(self, label = 'STOP')
        coil_boxsizer.Add(coil_stop, pos=(6,2), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)

        sbs_coil.Add(coil_boxsizer, border=5)
        sizer.Add(sbs_coil, pos=(8,1), border=5)
        ##########
        sb_spm = wx.StaticBox(self, label='Step Motor')
        sbs_spm = wx.StaticBoxSizer(sb_spm)
        spm_boxsizer = wx.GridBagSizer(5,5)

        spm_list = ['Speed','Position']
        self.spm_textctrl = []
        for i in range(2) :
            spm_boxsizer.Add(wx.StaticText(self, label=spm_list[i]), pos=(i,0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)
            self.spm_textctrl.append(wx.TextCtrl(self))
            spm_boxsizer.Add(self.spm_textctrl[-1], pos=(i,1), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=5)

        set_spm = wx.Button(self, label='Set')
        set_spm.Bind(wx.EVT_BUTTON, lambda event : self.write(cmd=f'MSPEED={self.spm_textctrl[0].GetValue()}'))
        spm_boxsizer.Add(set_spm, pos=(0,2), border=5)
        get_spm = wx.Button(self, label='Get')
        get_spm.Bind(wx.EVT_BUTTON, lambda event : self.write(cmd='GETMPOS'))
        spm_boxsizer.Add(get_spm, pos=(1,2), border=5)
        
        spm_run = wx.Button(self, label='Run')
        spm_run.Bind(wx.EVT_BUTTON, lambda event : self.write(cmd=f'MPOS={self.spm_textctrl[1].GetValue()}'))
        spm_boxsizer.Add(spm_run, pos=(2,0), flag=wx.ALIGN_CENTRE, border=5)
        spm_stop = wx.Button(self, label='Stop')
        spm_stop.Bind(wx.EVT_BUTTON, lambda event : self.write(cmd='MSTOP'))
        spm_boxsizer.Add(spm_stop, pos=(2,1), flag=wx.ALIGN_CENTRE, border=5)
        spm_gohome = wx.Button(self, label='Go Home')
        spm_gohome.Bind(wx.EVT_BUTTON, lambda event : self.write(cmd='GOHOME'))
        spm_boxsizer.Add(spm_gohome, pos=(2,2), flag=wx.ALIGN_CENTRE, border=5)

        sbs_spm.Add(spm_boxsizer, border=5)
        sizer.Add(sbs_spm, pos=(8,2), border=5)
        ##########

        hbox.Add(sizer, 0, wx.ALL|wx.ALIGN_CENTER)
        vbox.Add(hbox, 1, wx.ALL|wx.ALIGN_CENTER, 5)
        self.SetSizerAndFit(vbox)
        vbox.Fit(self)


    def get_par_fun(self) :

        for st in self.textctrl : st.SetValue('')
        command = ['GETCHO','GETCHF','GETCHD','GETCHC']
        for cmd in command :
            self.write(cmd)

    def set_par_fun(self) :
        for sp in ['CHO','CHF','CHD','CHC'] :
            self.setpa(params=sp)

    def setpa(self, params) :
        def fun(index, p) :
            cmd = ''
            for i,j in zip(index,range(1,7)) : 
                try : 
                    value = int(self.textctrl[i].GetValue())
                    cmd += f'{p}{j}={value};'
                except ValueError : pass
            return cmd
        command = ''
        if params == 'CHO' :
            for k,v in enumerate(self.cho) : command += f'{params}N{k+1}={int(v.GetValue())};'
        elif params == 'CHF' :
            index = [0,3,6,9,12,15]
            command += fun(index, params)
        elif params == 'CHD' :
            index = [1,4,7,10,13,16]
            command += fun(index, params)
        elif params == 'CHC' : 
            index = [2,5,8,11,14,17]
            command += fun(index, params)
        # print(command)
        self.write(command)
            
    def setch(self, channel) :
        command = (f'CHNO{channel}={int(self.cho[channel-1].GetValue())};'
            f'CHF{channel}={self.textctrl[channel*3-3].GetValue()};'
            f'CHD{channel}={self.textctrl[channel*3-2].GetValue()};'
            f'CHD{channel}={self.textctrl[channel*3-2].GetValue()};'
            f'CHC{channel}={self.textctrl[channel*3-1].GetValue()};')
        self.write(command)


    def get_checksum(self, msg) :
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

    def read(self) :
        print('recv ... ')
        t2 = threading.current_thread()
        while t2.open :
            try :
                if self.send_msg == 'MSTOP' : self.event.set()
                rec = self.epin.read(64)
                lrec = list(rec)
                LEN = lrec[0]
                msg = lrec[1:LEN-1]
                checksum = lrec[LEN-1]
                if self.get_checksum(msg) == checksum :
                    self.event.set()
                    data = ''.join([chr(x) for x in list(msg)])
                    data = data.split(',')
                    data = [x[5:] for x in data]
                    if self.send_msg == 'GETCHO' : 
                        for k,v in enumerate(data) : self.cho[k].SetValue(int(v))
                    elif self.send_msg == 'GETCHF' : 
                        for k,v in enumerate(data) : self.textctrl[k*3].SetValue(v)
                    elif self.send_msg == 'GETCHD' : 
                        for k,v in enumerate(data) : self.textctrl[k*3+1].SetValue(v)
                    elif self.send_msg == 'GETCHC' : 
                        for k,v in enumerate(data) : self.textctrl[k*3+2].SetValue(v)
                    elif self.send_msg == 'GETMPOS': self.spm_textctrl[1].SetValue(data[0])
                        
                else :
                    print(''.join([chr(x) for x in list(lrec)]))
            except usb.core.USBTimeoutError :
                pass

    def write(self, cmd) :
        self.event.clear()
        itera = 0
        self.send_msg = cmd
        # print(self.send_msg)
        cmd_data = list(bytearray(cmd.encode('ascii')))
        cmdchecksum = self.get_checksum(cmd_data)
        snd_cmd = [len(cmd)+2]+cmd_data+[cmdchecksum]
        while not self.event.is_set() and itera < 3:
            itera += 1
            self.epout.write(snd_cmd)
            self.event.wait(0.3)
        if itera == 3 :
            print('timeout')