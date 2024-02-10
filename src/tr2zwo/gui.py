#!/usr/bin/env python3
import wx

#==============================================================================
class Gui(wx.Frame):

  def __init__(self, parent, title):
    super(Gui, self).__init__(parent, title=title, size=(350, 250))
    self.Center()
    self.init_menu()

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
