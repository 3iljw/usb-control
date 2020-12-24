import copy
import csv
import datetime
import threading
import time

import usb
import wx


############################################

class Motor(wx.Panel) :
    """SP motor setting and action tab page setting."""
    def __init__(self, parent, mainFrame) :
        """SP motor setting and action tab page setting inital."""

        self.mainFrame = mainFrame

        wx.Panel.__init__(self, parent)
        sizer = wx.GridBagSizer(10, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox.Add(sizer, 0, wx.ALL|wx.ALIGN_CENTER)
        vbox.Add(hbox, 1, wx.ALL|wx.ALIGN_CENTER, 5)
        self.SetSizerAndFit(vbox)
        vbox.Fit(self)