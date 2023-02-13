import subprocess
import os
import sys
import gi
import faulthandler
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from threading import Thread
from gi.repository import Gtk, Adw, GLib


# Great segfault debugger
# faulthandler.enable()


# Appends variable amount of objects to the given parent
def multi_append(parent, *args):
    for obj in args:
        parent.append(obj)
# Sets sensitiity of multiple gtk widgets at once
def set_sens_multi(bool, *args):
    for obj in args:
        obj.set_sensitive(bool)


# Interface class to read values and run commands in Dell DCC CCTK
class CctkInterface:
    # Interface construction including values to remember the current active
    # radio buttons to only make the necessary changes in DCC
    def __init__(self, win):
        self.win = win
        self.cmd = "sudo /opt/dell/dcc/cctk "
        self.last_radio_thermal = object
        self.last_radio_battery = object
        self.last_custom_start = 0
        self.last_custom_stop = 0
        self.last_dropdown_kbd_ac = 0
        self.last_dropdown_kbd_bat = 0

    # Threadstarter for read_values()
    def start_read_values(self, start_obj):
        th = Thread(target=self.read_values)
        th.start()

    # Threadstarter for set_values()
    def start_set_values(self, start_obj):
        th = Thread(target=self.set_values)
        th.start()

    # Reads initial values from BIOS
    def read_values(self):
        self.win.send_msg(1, "Reading values...")
        ok_thermal = False
        ok_bat = False
        ok_kbd = False
        res_thermal = os.popen(
            self.cmd + "--ThermalManagement").read().replace("\n", "")
        # Reads thermal management option
        if res_thermal == "ThermalManagement=Optimized":
            self.win.radio_optimized.set_active(True)
            self.last_radio_thermal = self.win.radio_optimized
            ok_thermal = True
        elif res_thermal == "ThermalManagement=Cool":
            self.win.radio_cool.set_active(True)
            self.last_radio_thermal = self.win.radio_cool
            ok_thermal = True
        elif res_thermal == "ThermalManagement=Quiet":
            self.win.radio_quiet.set_active(True)
            self.last_radio_thermal = self.win.radio_quiet
            ok_thermal = True
        elif res_thermal == "ThermalManagement=UltraPerformance":
            self.win.radio_ultra.set_active(True)
            self.last_radio_thermal = self.win.radio_ultra
            ok_thermal = True
        # Reads battery charge config
        res_battery = os.popen(
            self.cmd + "--PrimaryBattChargeCfg").read().replace("\n", "")
        if res_battery == "PrimaryBattChargeCfg=Adaptive":
            self.win.radio_adaptive.set_active(True)
            self.last_radio_battery = self.win.radio_adaptive
            ok_bat = True
        elif res_battery == "PrimaryBattChargeCfg=Standard":
            self.win.radio_standard.set_active(True)
            self.last_radio_battery = self.win.radio_standard
            ok_bat = True
        elif res_battery == "PrimaryBattChargeCfg=PrimAcUse":
            self.win.radio_prim_ac.set_active(True)
            self.last_radio_battery = self.win.radio_prim_ac
            ok_bat = True
        elif res_battery == "PrimaryBattChargeCfg=Express":
            self.win.express_charge.set_active(True)
            self.last_radio_battery = self.win.express_charge
            ok_bat = True
        elif res_battery.split(':')[0] == "PrimaryBattChargeCfg=Custom":
            res_battery = res_battery.split(':')
            start_stop = res_battery[1].split('-')
            self.last_custom_start = start_stop[0]
            self.last_custom_stop = start_stop[1]
            self.win.entry_start_treshold.get_buffer().set_text(
                self.last_custom_start,
                len(self.last_custom_start)
            )
            self.win.entry_stop_treshold.get_buffer().set_text(
                self.last_custom_stop,
                len(self.last_custom_stop)
            )
            self.win.radio_custom.set_active(True)
            self.last_radio_battery = self.win.radio_custom
            self.win.entry_start_treshold.set_placeholder_text("")
            self.win.entry_stop_treshold.set_placeholder_text("")
            ok_bat = True
        # Reads keyboard backlight settings for AC
        res_kbd_ac = os.popen(
            self.cmd + "--KbdBacklightTimeoutAc").read().replace("\n", "")
        if res_kbd_ac.split('=')[-1] == "5s":
            self.last_dropdown_kbd_ac = 0
            ok_kbd = True
            self.win.dropdown_kbd_ac.set_selected(0)
        elif res_kbd_ac.split('=')[-1] == "10s":
            self.last_dropdown_kbd_ac = 1
            ok_kbd = True
            self.win.dropdown_kbd_ac.set_selected(1)
        elif res_kbd_ac.split('=')[-1] == "15s":
            self.last_dropdown_kbd_ac = 2
            ok_kbd = True
            self.win.dropdown_kbd_ac.set_selected(2)
        elif res_kbd_ac.split('=')[-1] == "30s":
            self.last_dropdown_kbd_ac = 3
            ok_kbd = True
            self.win.dropdown_kbd_ac.set_selected(3)
        elif res_kbd_ac.split('=')[-1] == "1m":
            self.last_dropdown_kbd_ac = 4
            ok_kbd = True
            self.win.dropdown_kbd_ac.set_selected(4)
        elif res_kbd_ac.split('=')[-1] == "5m":
            self.last_dropdown_kbd_ac = 5
            ok_kbd = True
            self.win.dropdown_kbd_ac.set_selected(5)
        elif res_kbd_ac.split('=')[-1] == "15m":
            self.last_dropdown_kbd_ac = 6
            ok_kbd = True
            self.win.dropdown_kbd_ac.set_selected(6)
        elif res_kbd_ac.split('=')[-1] == "Never":
            self.last_dropdown_kbd_ac = 7
            ok_kbd = True
            self.win.dropdown_kbd_ac.set_selected(7)  
        # Reads keyboard backlight settings for BAT
        res_kbd_bat = os.popen(
            self.cmd + "--KbdBacklightTimeoutBatt").read().replace("\n", "")
        if res_kbd_bat.split('=')[-1] == "5s":
            self.last_dropdown_kbd_bat = 0
            ok_kbd = True
            self.win.dropdown_kbd_bat.set_selected(0)
        elif res_kbd_bat.split('=')[-1] == "10s":
            self.last_dropdown_kbd_bat = 1
            ok_kbd = True
            self.win.dropdown_kbd_bat.set_selected(1)
        elif res_kbd_bat.split('=')[-1] == "15s":
            self.last_dropdown_kbd_bat = 2
            ok_kbd = True
            self.win.dropdown_kbd_bat.set_selected(2)
        elif res_kbd_bat.split('=')[-1] == "30s":
            self.last_dropdown_kbd_bat = 3
            ok_kbd = True
            self.win.dropdown_kbd_bat.set_selected(3)
        elif res_kbd_bat.split('=')[-1] == "1m":
            self.last_dropdown_kbd_bat = 4
            ok_kbd = True
            self.win.dropdown_kbd_bat.set_selected(4)
        elif res_kbd_bat.split('=')[-1] == "5m":
            self.last_dropdown_kbd_bat = 5
            ok_kbd = True
            self.win.dropdown_kbd_bat.set_selected(5)
        elif res_kbd_bat.split('=')[-1] == "15m":
            self.last_dropdown_kbd_bat = 6
            ok_kbd = True
            self.win.dropdown_kbd_bat.set_selected(6)
        elif res_kbd_bat.split('=')[-1] == "Never":
            self.last_dropdown_kbd_bat = 7
            ok_kbd = True
            self.win.dropdown_kbd_bat.set_selected(7)
        # Checks whether values were read successfully
        # and disables settings that are not available
        if ok_thermal or ok_bat or ok_kbd:
            self.win.send_msg(0, "Successfully read values")
            if not ok_thermal:
                set_sens_multi(
                    False,
                    self.win.lbl_therm_manag,
                    self.win.radio_optimized,
                    self.win.radio_cool,
                    self.win.radio_quiet,
                    self.win.radio_ultra
                )
            if not ok_bat:
                set_sens_multi(
                    False,
                    self.win.lbl_batt_charge_conf,
                    self.win.radio_adaptive,
                    self.win.radio_standard,
                    self.win.radio_prim_ac,
                    self.win.express_charge,
                    self.win.radio_custom,
                    self.win.box_entry_tresholds
                )
            if not ok_kbd:
                set_sens_multi(
                    False,
                    self.win.lbl_kbd,
                    self.win.dropdown_kbd_ac,
                    self.win.dropdown_kbd_bat
                )
        else:
            self.win.send_msg(
                0, "Error fetching values. Check if DCC is installed and accessable")

    # Sets values in bios via DCC
    def set_values(self):
        self.win.send_msg(1, "Setting values...")
        ok_thermal = False
        ok_bat = False
        ok_kbd = False
        err = False
        # Set thermal management option
        if self.win.radio_optimized.get_active() and \
                self.win.radio_optimized != self.last_radio_thermal:
            self.last_radio_thermal = self.win.radio_optimized
            res = subprocess.call(
                self.cmd + "--ThermalManagement=Optimized", shell=True)
            if res == 0:
                ok_thermal = True
        elif self.win.radio_cool.get_active() and \
                self.win.radio_cool != self.last_radio_thermal:
            self.last_radio_thermal = self.win.radio_cool
            res = subprocess.call(
                self.cmd + "--ThermalManagement=Cool", shell=True)
            if res == 0:
                ok_thermal = True
        elif self.win.radio_quiet.get_active() and \
                self.win.radio_quiet != self.last_radio_thermal:
            self.last_radio_thermal = self.win.radio_quiet
            res = subprocess.call(
                self.cmd + "--ThermalManagement=Quiet", shell=True)
            if res == 0:
                ok_thermal = True
        elif self.win.radio_ultra.get_active() and \
                self.win.radio_ultra != self.last_radio_thermal:
            self.last_radio_thermal = self.win.radio_ultra
            res = subprocess.call(
                self.cmd + "--ThermalManagement=UltraPerformance", shell=True)
            if res == 0:
                ok_thermal = True
        # print(f"ok_thermal: {ok_thermal}, ok_bat: {ok_bat}")
        # Set battery charge config
        if self.win.radio_adaptive.get_active() and \
                self.win.radio_adaptive != self.last_radio_battery:
            self.last_radio_battery = self.win.radio_adaptive
            res = subprocess.call(
                self.cmd + "--PrimaryBattChargeCfg=Adaptive", shell=True)
            if res == 0:
                ok_bat = True
        elif self.win.radio_standard.get_active() and \
                self.win.radio_standard != self.last_radio_battery:
            self.last_radio_battery = self.win.radio_standard
            res = subprocess.call(
                self.cmd + "--PrimaryBattChargeCfg=Standard", shell=True)
            if res == 0:
                ok_bat = True
        elif self.win.radio_prim_ac.get_active() and \
                self.win.radio_prim_ac != self.last_radio_battery:
            self.last_radio_battery = self.win.radio_prim_ac
            res = subprocess.call(
                self.cmd + "--PrimaryBattChargeCfg=PrimAcUse", shell=True)
            if res == 0:
                ok_bat = True
        elif self.win.express_charge.get_active() and \
                self.win.express_charge != self.last_radio_battery:
            self.last_radio_battery = self.win.express_charge
            res = subprocess.call(
                self.cmd + "--PrimaryBattChargeCfg=Express", shell=True)
            if res == 0:
                ok_bat = True
        elif self.win.radio_custom.get_active():
            # Validate custom tresholds
            try:
                start_tres = round(
                    float(self.win.entry_start_treshold.get_buffer().get_text()))
                stop_tres = round(
                    float(self.win.entry_stop_treshold.get_buffer().get_text()))
                if start_tres < stop_tres:
                    if stop_tres - start_tres >= 5:
                        if start_tres >= 50 and start_tres <= 95:
                            if stop_tres >= 55 and stop_tres <= 100:
                                if self.last_custom_start != start_tres or self.last_custom_stop != stop_tres \
                                    or self.last_radio_battery != self.win.radio_custom:
                                    self.last_radio_battery = self.win.radio_custom
                                    self.last_custom_start = start_tres
                                    self.last_custom_stop = stop_tres
                                    cmd_custom = f"--PrimaryBattChargeCfg=Custom:{start_tres}-{stop_tres}"
                                    res = subprocess.call(
                                        self.cmd + cmd_custom, shell=True)
                                    if res == 0:
                                        ok_bat = True
                                else:
                                    err = True
                                    self.win.send_msg(
                                    0, "Values not set. No changes detected")
                            else:
                                err = True
                                self.win.send_msg(
                                    0, "Error: Stop treshold cannot be less than 55 or more than 100")
                        else:
                            err = True
                            self.win.send_msg(
                                0, "Error: Start treshold cannot be less than 50 or more than 95")
                    else:
                        err = True
                        self.win.send_msg(
                            0, "Error: Difference between start en stop treshold should be 5 or more")
                else:
                    err = True
                    self.win.send_msg(
                        0, "Error: Start treshold cannot be more than stop treshold")
            except Exception as e:
                print(e)
                err = True
                self.win.send_msg(0, "Error: Check custom treshold formatting")
        # Set keyboard backlight config for AC
        if self.win.dropdown_kbd_ac.get_selected() == 0 and \
                self.win.dropdown_kbd_ac.get_selected() != self.last_dropdown_kbd_ac:
            self.last_dropdown_kbd_ac = 0
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutAc=5s", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_ac.get_selected() == 1 and \
                self.win.dropdown_kbd_ac.get_selected() != self.last_dropdown_kbd_ac:
            self.last_dropdown_kbd_ac = 1
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutAc=10s", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_ac.get_selected() == 2 and \
                self.win.dropdown_kbd_ac.get_selected()!= self.last_dropdown_kbd_ac:
            self.last_dropdown_kbd_ac = 2
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutAc=15s", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_ac.get_selected() == 3 and \
                self.win.dropdown_kbd_ac.get_selected() != self.last_dropdown_kbd_ac:
            self.last_dropdown_kbd_ac = 3
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutAc=30s", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_ac.get_selected() == 4 and \
                self.win.dropdown_kbd_ac.get_selected() != self.last_dropdown_kbd_ac:
            self.last_dropdown_kbd_ac = 4
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutAc=1m", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_ac.get_selected() == 5 and \
                self.win.dropdown_kbd_ac.get_selected() != self.last_dropdown_kbd_ac:
            self.last_dropdown_kbd_ac = 5
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutAc=5m", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_ac.get_selected() == 6 and \
                self.win.dropdown_kbd_ac.get_selected() != self.last_dropdown_kbd_ac:
            self.last_dropdown_kbd_ac = 6
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutAc=15m", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_ac.get_selected() == 7 and \
                self.win.dropdown_kbd_ac.get_selected() != self.last_dropdown_kbd_ac:
            self.last_dropdown_kbd_ac = 7
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutAc=Never", shell=True)
            if res == 0:
                ok_kbd = True
        # Set keyboard backlight config for battery
        if self.win.dropdown_kbd_bat.get_selected() == 0 and \
                self.win.dropdown_kbd_bat.get_selected() != self.last_dropdown_kbd_bat:
            self.last_dropdown_kbd_bat = 0
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutBatt=5s", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_bat.get_selected() == 1 and \
                self.win.dropdown_kbd_bat.get_selected() != self.last_dropdown_kbd_bat:
            self.last_dropdown_kbd_bat = 1
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutBatt=10s", shell=True)
            if res == 0:    
                ok_kbd = True
        elif self.win.dropdown_kbd_bat.get_selected() == 2 and \
                self.win.dropdown_kbd_bat.get_selected() != self.last_dropdown_kbd_bat:
            self.last_dropdown_kbd_bat = 2
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutBatt=15s", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_bat.get_selected() == 3 and \
                self.win.dropdown_kbd_bat.get_selected() != self.last_dropdown_kbd_bat:
            self.last_dropdown_kbd_bat = 3
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutBatt=30s", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_bat.get_selected() == 4 and \
                self.win.dropdown_kbd_bat.get_selected() != self.last_dropdown_kbd_bat:
            self.last_dropdown_kbd_bat = 4
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutBatt=1m", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_bat.get_selected() == 5 and \
                self.win.dropdown_kbd_bat.get_selected() != self.last_dropdown_kbd_bat:
            self.last_dropdown_kbd_bat = 5
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutBatt=5m", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_bat.get_selected() == 6 and \
                self.win.dropdown_kbd_bat.get_selected() != self.last_dropdown_kbd_bat:
            self.last_dropdown_kbd_bat = 6
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutBatt=15m", shell=True)
            if res == 0:
                ok_kbd = True
        elif self.win.dropdown_kbd_bat.get_selected() == 7 and \
                self.win.dropdown_kbd_bat.get_selected() != self.last_dropdown_kbd_bat:
            self.last_dropdown_kbd_bat = 7
            res = subprocess.call(
                self.cmd + "--KbdBacklightTimeoutBatt=Never", shell=True)
            if res == 0:
                ok_kbd = True
        # Checks if everything went ok
        if ok_thermal or ok_bat or ok_kbd and not err:
            self.win.send_msg(0, "Successfully applied changes")
        elif err:
            pass
        else:
            self.win.send_msg(
                0, "Values not set. No changes detected")


class MainWindow (Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs
        )
        # Set application name
        GLib.set_prgname('Dell Command Center')
        GLib.set_application_name('Dell Command Center')
        # Main box
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.box_main)
        # Headerbar
        self.hb = Gtk.HeaderBar()
        self.box_main.append(self.hb)
        # Create status in topbar
        self.statusbox = Gtk.Box()
        self.lbl_status = Gtk.Label(
            label="",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.spinner = Gtk.Spinner()
        multi_append(
            self.statusbox,
            self.spinner,
            self.lbl_status
        )
        self.hb.set_title_widget(self.statusbox)
        # Clamp widget
        self.clamp_main = Adw.Clamp()
        self.box_main.append(self.clamp_main)
        # Wrapper inside Adw.Clamp
        self.box_wrapper_main = Gtk.Box(
            spacing=10,
            margin_start=20,
            margin_end=20,
            margin_top=20,
            margin_bottom=20,
            orientation=Gtk.Orientation.VERTICAL
        )
        self.clamp_main.set_child(self.box_wrapper_main)
        ########################################
        # Category: Thermal Management         #
        ########################################
        # Performance and battery label
        self.lbl_perf_and_batt = Gtk.Label(
            label='Performance and battery',
            halign=Gtk.Align.CENTER,
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.lbl_perf_and_batt.get_style_context().add_class('title-4')
        self.lbl_perf_and_batt.set_wrap(True)
        self.box_wrapper_main.append(self.lbl_perf_and_batt)
        # Thermal management box
        self.box_power_batt = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box_power_batt.get_style_context().add_class('card')
        self.box_wrapper_main.append(self.box_power_batt)
        # Label inside power_batt box
        self.lbl_therm_manag = Gtk.Label(
            label="Thermal management",
            margin_start=10,
            margin_end=10,
            margin_top=15,
            margin_bottom=5,
        )
        # Box for radio buttons for thermal management
        self.box_radio_thermal = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            halign=Gtk.Align.CENTER,
            margin_start=15,
            margin_end=15,
            margin_top=5,
            margin_bottom=5,
        )
        # Radio button group for thermal management
        self.radio_optimized = Gtk.CheckButton(
            label="Optimized",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.radio_cool = Gtk.CheckButton(
            label="Cool",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.radio_quiet = Gtk.CheckButton(
            label="Quiet",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.radio_ultra = Gtk.CheckButton(
            label="Ultra Performance",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.radio_cool.set_group(self.radio_optimized)
        self.radio_quiet.set_group(self.radio_optimized)
        self.radio_ultra.set_group(self.radio_optimized)
        # Adds radiogroup to thermal box
        multi_append(
            self.box_radio_thermal,
            self.radio_optimized,
            self.radio_cool,
            self.radio_quiet,
            self.radio_ultra
        )
        self.box_power_batt.append(self.lbl_therm_manag)
        self.box_power_batt.append(self.box_radio_thermal)
        ###########################################
        # Category: Primary Battery Charge Config #
        ###########################################
        # Label for battery charge config
        self.lbl_batt_charge_conf = Gtk.Label(
            label="Primary battery charge configuration",
            margin_start=10,
            margin_end=10,
            margin_top=15,
            margin_bottom=5,
        )
        # Box for radio buttons for primary battery charge config
        self.box_radio_batt_charge_conf = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            halign=Gtk.Align.CENTER,
            margin_start=15,
            margin_end=15,
            margin_top=5,
            margin_bottom=5,
        )
        # Radio button group for primary battery charge config
        self.radio_adaptive = Gtk.CheckButton(
            label="Adaptive",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.radio_standard = Gtk.CheckButton(
            label="Standard",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.radio_prim_ac = Gtk.CheckButton(
            label="Primarily AC use",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.express_charge = Gtk.CheckButton(
            label="ExpressCharge",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.radio_custom = Gtk.CheckButton(
            label="Custom",
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.radio_standard.set_group(self.radio_adaptive)
        self.radio_prim_ac.set_group(self.radio_adaptive)
        self.express_charge.set_group(self.radio_adaptive)
        self.radio_custom.set_group(self.radio_adaptive)
        # Adds radiogroup to battery box
        multi_append(
            self.box_radio_batt_charge_conf,
            self.radio_adaptive,
            self.radio_standard,
            self.radio_prim_ac,
            self.express_charge,
            self.radio_custom
        )
        # Textfields for charging tresholds
        self.box_entry_tresholds = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            halign=Gtk.Align.CENTER,
            margin_start=15,
            margin_end=15,
            margin_top=5,
            margin_bottom=5,
        )
        self.lbl_start_treshold = Gtk.Label(
            label='Start treshold:',
            halign=Gtk.Align.CENTER,
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.entry_start_treshold = Gtk.Entry()
        self.entry_start_treshold.set_placeholder_text("50-95")
        self.entry_start_treshold.set_max_length(3)
        self.lbl_stop_Treshold = Gtk.Label(
            label='Stop treshold:',
            halign=Gtk.Align.CENTER,
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.entry_stop_treshold = Gtk.Entry()
        self.entry_stop_treshold.set_placeholder_text("55-100")
        self.entry_stop_treshold.set_max_length(3)
        #################################
        # Category: Keyboard backlight  #
        #################################
        # Label for keyboard backlight
        self.lbl_kbd = Gtk.Label(
            label="Keyboard backlight timeout",
            margin_start=10,
            margin_end=10,
            margin_top=15,
            margin_bottom=5,
        )
        # Dropdown options for kbd backlight
        self.kbd_options = [
            "5s",
            "10s",
            "15s",
            "30s",
            "1m",
            "5m",
            "15m",
            "Never"
        ]
        # Dropdowns for kbd backlight
        self.dropdown_kbd_ac = Gtk.DropDown.new_from_strings(self.kbd_options)
        self.dropdown_kbd_bat = Gtk.DropDown.new_from_strings(self.kbd_options)
        # Labels for kbd backlight dropdowns
        self.lbl_kbd_ac = Gtk.Label(
            label="AC:",
            halign=Gtk.Align.CENTER,
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        self.lbl_kbd_bat = Gtk.Label(
            label="Battery:",
            halign=Gtk.Align.CENTER,
            margin_start=5,
            margin_end=5,
            margin_top=5,
            margin_bottom=5,
        )
        # Hbox for AC kbd dropdown
        self.kbd_ac_hbox = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            halign=Gtk.Align.CENTER,
            margin_start=15,
            margin_end=15,
            margin_top=5,
            margin_bottom=5
        )
        multi_append(self.kbd_ac_hbox, self.lbl_kbd_ac, self.dropdown_kbd_ac)
        # Hbox for battery kbd dropdown
        self.kbd_bat_hbox = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            halign=Gtk.Align.CENTER,
            margin_start=15,
            margin_end=15,
            margin_top=5,
            margin_bottom=5
        )
        multi_append(self.kbd_bat_hbox, self.lbl_kbd_bat, self.dropdown_kbd_bat)
        # Hbox for keyboard dropdowns
        self.kbd_hbox = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=100,
            halign=Gtk.Align.CENTER,
            margin_start=15,
            margin_end=15,
            margin_top=5,
            margin_bottom=5
            )
        multi_append(self.kbd_hbox, self.kbd_ac_hbox, self.kbd_bat_hbox)
        # Vbox for keyboard dropdowns
        self.kbd_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.CENTER, margin_bottom=5)
        multi_append(self.kbd_vbox, self.lbl_kbd, self.kbd_hbox)
        # Buttons to apply/discard changes
        self.button_box = Gtk.Box(
            halign=Gtk.Align.CENTER,
            spacing=100,
            margin_start=10,
            margin_end=10,
            margin_top=20,
            margin_bottom=20
        )
        self.discard_button = Gtk.Button(label='Discard changes and reload')
        self.discard_button.get_style_context().add_class('destructive-action')
        self.button_box.append(self.discard_button)
        self.apply_button = Gtk.Button(label='Apply changes')
        self.apply_button.get_style_context().add_class('suggested-action')
        self.button_box.append(self.apply_button)
        multi_append(
            self.box_entry_tresholds,
            self.lbl_start_treshold,
            self.entry_start_treshold,
            self.lbl_stop_Treshold,
            self.entry_stop_treshold
        )
        # Adds elements to clamp
        multi_append(
            self.box_power_batt,
            self.lbl_batt_charge_conf,
            self.box_radio_batt_charge_conf,
            self.box_entry_tresholds,
            self.kbd_vbox
        )
        # Adds elements outside of clamp
        self.box_main.append(self.button_box)
        # Starts interface
        self.cctk_interface = CctkInterface(self)
        self.cctk_interface.read_values()
        self.discard_button.connect(
            "clicked", self.cctk_interface.start_read_values
        )
        self.apply_button.connect(
            "clicked", self.cctk_interface.start_set_values
        )

    # Set status in topheader
    def send_msg(self, work_status, msg):
        if work_status == 1:
            self.spinner.start()
        else:
            self.spinner.stop()
        self.lbl_status.set_text(msg)


class MyApp (Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.connect(
            'activate',
            self.on_activate
        )

    def on_activate(self, app):
        self.win = MainWindow(
            application=app
        )
        self.win.present()


app = MyApp(
    application_id='io.github.DimseBoms.dell-command-center'
)
# Checks for install flag and adds .desktop entry
install = False
for arg in sys.argv:
    arg = str(arg)
    if arg == "--install":
        install = True
        home_dir = os.environ['HOME']
        with open(f"{home_dir}/.local/share/applications/dcc-gui.desktop", 'w') as desktop_file:
            desktop_file.write(
                "[Desktop Entry]\n" +
                "Encoding=UTF-8\n" +
                "Type=Application\n" +
                "Terminal=false\n" +
                f"Exec=/usr/bin/python3 {os.getcwd()}/main.py\n" +
                "Name=Dell Command Configure GUI\n" +
                f"Icon={os.getcwd()}/logo.png\n"
            )
# Runs normally
if not install:
    app.run(sys.argv)

# TODO: Add polkit rules so the application can be run with pkexec
# TODO: Move styling to stylesheets
