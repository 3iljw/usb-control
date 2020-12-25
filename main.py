import wx
from light import LED
from vp import Motor


class MainFrame(wx.Frame):
    """Main Frame."""
    def __init__(self):

        wx.Frame.__init__(self, None, title="USB control", size=(900, 600))


        # Create a panel and notebook (tabs holder)
        page = wx.Panel(self)
        pgnb = wx.Notebook(page, size=(800,500))
        # self.pnl = wx.Panel(page)
        
        # Create the tab windows
        self.tab1 = Motor(pgnb, self)
        self.tab2 = LED(pgnb, self)

        # Add the windows to tabs and name them.
        pgnb.AddPage(self.tab1, "Vibration Control")
        pgnb.AddPage(self.tab2, "Light Control")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(pgnb, -1, wx.EXPAND)
        # sizer.Add(self.pnl, -1)

        page.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.close)
        self.Center()
    
    def close(self, event) :
        self.tab1.read_thread.open = False
        self.tab1.read_thread.join()
        self.tab2.read_thread.open = False 
        self.tab2.read_thread.join()

        self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
