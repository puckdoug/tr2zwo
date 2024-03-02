#!/usr/bin/env python3
import wx
import wx.html2
from tr2zwo import TRFetch, Workout, TRConfig

#==============================================================================
class Gui(wx.Frame):
  browser = wx.html2.WebView

  def __init__(self, parent, title):
    super(Gui, self).__init__(parent, title=title, size=(1000, 1200))
    self.Center()
    self.init_menu()
    self.draw_panel()
    self.load_trainerroad()

#----------------------------------------------------------------------
  def load_trainerroad(self):
    self.browser.LoadURL("https://www.trainerroad.com/")

#----------------------------------------------------------------------
  def draw_panel(self):
    panel = wx.Panel(self)
    box = wx.BoxSizer(wx.HORIZONTAL)
    fgs = wx.FlexGridSizer(rows=2, cols=2, vgap=10, hgap=10)

    #fgs.AddGrowableRow(0,1) # Make row 1 growable
    url_label = wx.StaticText(parent=panel, label="URL:")
    url = wx.TextCtrl(parent=panel, size=(900, -1), style=wx.TE_DONTWRAP)
    url.SetFocus()
    fetch_button = wx.Button(parent=panel, label="Fetch", )
    fetch_button.Bind(wx.EVT_BUTTON, self.on_click)
    fgs.Add(window=url_label, proportion=0, flag=wx.ALIGN_LEFT)
    fgs.Add(window=url, proportion=1, flag=wx.ALIGN_RIGHT|wx.EXPAND)
    fgs.Add(window=fetch_button, proportion=0, flag=wx.ALIGN_RIGHT)

    #fgs.AddGrowableRow(1,1)

    fgs.AddGrowableRow(1,1) # Make row 2 growable
    self.browser = wx.html2.WebView.New(parent=panel)
    fgs.Add(window=self.browser, proportion=1, flag=wx.EXPAND)

    box.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
    panel.SetSizer(box)

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
  def on_click(self, event):
    url = self.browser.GetCurrentURL()

    f = TRFetch(verbose=True)
    c = TRConfig()
    c.verbose = True
    data = f.fetch_workout(url)
    w = Workout.create(raw=data, url=url, verbose=True)
    w.write(directory=c.directory)

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
