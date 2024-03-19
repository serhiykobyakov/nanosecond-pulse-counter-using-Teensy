#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__version__ = '19.03.2024'
__author__ = 'Serhiy Kobyakov'

import sys
import wx
from arduino_device import ArduinoDevice as AD
from photoncounter import PhotonCounter

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
    def __init__(self, the_counter, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        # ~ self.SetTitle("test Photon Counter")
        self.the_counter = the_counter

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        # 1st row of controls
        sizer_top = wx.BoxSizer(wx.HORIZONTAL)

        # Button start / stop
        self.button_toggle_run = wx.ToggleButton(self.panel_1,
                                                 wx.ID_ANY,
                                                 "Continuous")
        sizer_top.Add(self.button_toggle_run, 0, wx.ALL, 5)

        self.count_label = wx.StaticText(self.panel_1,
                                         label="",
                                         style=wx.ALIGN_RIGHT)
        self.count_label.SetMinSize(wx.Size(250, -1))
        self.count_label.SetFont(wx.Font(30,
                                         wx.DEFAULT,
                                         wx.NORMAL,
                                         wx.NORMAL))
        sizer_top.Add(self.count_label, 0, wx.ALL, 5)

        # 2nd row of controls
        self.gauge_1 = wx.Gauge(self.panel_1,
                                wx.ID_ANY,
                                800,
                                # ~ size=(800,100),
                                style=wx.GA_HORIZONTAL)
        self.gauge_1.SetMinSize((800, 30))
        self.update_gauge(0)

        sizer_main.Add(sizer_top, 0, wx.EXPAND, 0)
        sizer_main.Add(self.gauge_1, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.panel_1.SetSizer(sizer_main)

        sizer_main.Fit(self)
        self.Layout()

        self.button_toggle_run.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_run)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        # end wxGlade

    def toggle_run(self, event):  # wxGlade: MainFrame.<event_handler>
        if self.button_toggle_run.GetValue():
            self.gauge_1.Show()
            self.button_toggle_run.SetLabel("Stop")
            self.timer = wx.Timer(self)
            self.timer.Start(200)
        else:
            self.timer.Stop()
            del self.timer
            self.gauge_1.SetValue(0)
            self.gauge_1.Hide()
            self.button_toggle_run.SetLabel("Continuous")
        event.Skip()

    def on_timer(self, event):
        self.update_gauge(self.the_counter.get_cps())

    def update_gauge(self, new_value):
        if new_value > self.gauge_1.GetRange():
            self.gauge_1.SetRange(round(new_value * 1.05))
        if new_value < self.gauge_1.GetRange() * 0.25:
            self.gauge_1.SetRange(round(new_value * 1.05))
        self.gauge_1.SetValue(round(new_value))
        the_label = "{:,d}".format(round(new_value)).replace(",", " ")
        self.count_label.SetLabel(the_label)
        wx.Yield()


class MyApp(wx.App):
    """the wx App"""
    theport = ''
    photon_counter = None

    def OnInit(self):
        """do some initializations before creating the App"""
        # check if photon counter available before starting the App
        dev_avail = AD.get_arduino_serial_devices_dict()
        print(f"found Photon Counter at {dev_avail["PhotonCounter"]}")
        if "PhotonCounter" not in dev_avail.keys():
            print("Please connect photon counter!")
            wx.MessageBox("""You need photon counter
to use this program.
Please connect it to PC
and/or check if it is powered!""",
                          "Error",
                          wx.OK | wx.ICON_ERROR)
            sys.exit(1)

        # if photon counter is connected - initialize the object
        self.photon_counter = PhotonCounter(dev_avail["PhotonCounter"])

        # exit App if photon counter has not been initialized:
        if self.photon_counter is None:
            print("Error during initialization of photon counter!")
            wx.MessageBox("""photon counter:
Error during initialization!""",
                          "Error",
                          wx.OK | wx.ICON_ERROR)
            sys.exit(1)

        self.frame = MainFrame(self.photon_counter,
                               None,
                               wx.ID_ANY,
                               "Photon Counter at " +
                               dev_avail["PhotonCounter"])
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
