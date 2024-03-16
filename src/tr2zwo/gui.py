#!/usr/bin/env python3
import wx
import wx.html2
from tr2zwo import TRFetch, Workout, TRConfig

#==============================================================================
class Gui(wx.Frame):
  browser = wx.html2.WebView

#----------------------------------------------------------------------
  def __init__( self, parent, title ):
    super(Gui, self).__init__(parent, title=title, size=wx.Size( 1000,1200 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
    self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
    self.init_menu()
    self.draw_frame_contents()
    self.Layout()
    self.Centre( wx.BOTH )
    self.load_trainerroad()

#----------------------------------------------------------------------
  def draw_frame_contents(self):
    # top row for navigation and status
    box = wx.BoxSizer( wx.VERTICAL )
    nav_sizer = wx.FlexGridSizer( 1, 5, 50, 5 )
    nav_sizer.AddGrowableCol( 3 )
    nav_sizer.SetFlexibleDirection( wx.HORIZONTAL )
    nav_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )
    self.bck_button = wx.Button( self, wx.ID_ANY, u"Back", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.bck_button.Bind(wx.EVT_BUTTON, self.do_back)
    self.fwd_button = wx.Button( self, wx.ID_ANY, u"Fwd", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.fwd_button.Bind(wx.EVT_BUTTON, self.do_fwd)
    self.fetch_button = wx.Button( self, wx.ID_ANY, u"Fetch", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.fetch_button.Bind(wx.EVT_BUTTON, self.do_fetch)
    self.status_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
    self.cfg_button = wx.Button( self, wx.ID_ANY, u"Config", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.cfg_button.Bind(wx.EVT_BUTTON, self.do_config)
    self.status_text.Enable( False )
    nav_sizer.Add( window=self.bck_button, proportion=0, flag=wx.LEFT )
    nav_sizer.Add( window=self.fwd_button, proportion=0, flag=wx.LEFT )
    nav_sizer.Add( window=self.fetch_button, proportion=0, flag=wx.LEFT )
    nav_sizer.Add( window=self.status_text, proportion=1, flag=wx.EXPAND )
    nav_sizer.Add( window=self.cfg_button, proportion=0, flag=wx.LEFT )
    box.Add( nav_sizer, 0, wx.EXPAND, 5 )

    # just the browser below
    browser_sizer = wx.FlexGridSizer( 1, 1, 0, 0 )
    browser_sizer.SetFlexibleDirection( wx.BOTH )
    browser_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
    browser_sizer.AddGrowableCol( 0 )
    browser_sizer.AddGrowableRow( 0 )

    self.browser = wx.html2.WebView.New(parent=self)
    browser_sizer.Add( self.browser, 1, wx.EXPAND, 5 )
    box.Add( browser_sizer, 1, wx.EXPAND, 5 )

    self.SetSizer( box )

#----------------------------------------------------------------------
  def load_trainerroad(self):
    self.browser.LoadURL("https://www.trainerroad.com/")

#----------------------------------------------------------------------
  def handle_new_windwow(self):
      #EVT_WEBVIEW_NEWWINDOW   wxEVT_WEBVIEW_NEWWINDOW
    pass
#----------------------------------------------------------------------
  def init_menu(self):
    menu_bar = wx.MenuBar()
    file_menu = wx.Menu()
    quit_menu_item = wx.MenuItem(file_menu, 1, '&Quit\tCtrl+Q')
    file_menu.Append(quit_menu_item)
    self.Bind(wx.EVT_MENU, self.on_quit, quit_menu_item)
    menu_bar.Append(file_menu, '&File')
    self.SetMenuBar(menu_bar)

#----------------------------------------------------------------------
  def do_fetch(self, event):
    url = self.browser.GetCurrentURL()

    f = TRFetch(verbose=True)
    c = TRConfig()
    c.verbose = True
    data = f.fetch_workout(url)
    w = Workout.create(raw=data, url=url, verbose=True)
    w.write(directory=c.directory)

#----------------------------------------------------------------------
  def do_back(self, event):
    print("Back clicked")

#----------------------------------------------------------------------
  def do_fwd(self, event):
    print("Forward clicked")

#----------------------------------------------------------------------
  def do_cfg(self, event):
    print("Config clicked")

#----------------------------------------------------------------------
  def on_quit(self, e):
    self.Close()

#==============================================================================
def main():
    app = wx.App()
    ex = Gui(None, title='TrainerRoad to Zwift')
    ex.Show()
    app.MainLoop()

#==============================================================================
if __name__ == '__main__':
    main()
