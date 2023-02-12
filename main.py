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
faulthandler.enable()


# Appends variable amount of objects to the given parent
def multi_append(parent, *args):
    for obj in args:
        parent.append(obj)


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
        if ok_thermal or ok_bat:
            self.win.send_msg(0, "Successfully read values")
        else:
            self.win.send_msg(
                0, "Error fetching values. Check if DCC is installed and accessable")

    # Sets values in bios via DCC
    def set_values(self):
        self.win.send_msg(1, "Setting values...")
        ok_thermal = False
        ok_bat = False
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
            self.last_radio_battery = self.win.radio_express_charge
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
        # print(f"ok_thermal: {ok_thermal}, ok_bat: {ok_bat}")
        if ok_thermal or ok_bat and not err:
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
        # Buttons to apply/discard changes
        self.button_box = Gtk.Box(
            halign=Gtk.Align.CENTER,
            spacing=100,
            margin_start=10,
            margin_end=10,
            margin_top=20,
            margin_bottom=20,
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
            self.box_entry_tresholds
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
# TODO: Add ability to control keyboard backlight settings
