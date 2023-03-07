from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QVBoxLayout, QHBoxLayout, QRadioButton, QSlider, QLabel, QPushButton, QStatusBar, QWidget
import sys, libsmbios_interface

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize libsmbios interface
        self.smbios = libsmbios_interface.LibsmbiosInterface()

        print(f"Thermal behavior: {self.smbios.read_thermal_behavior()}")

        self.setWindowTitle("My Application")
        self.setGeometry(300, 200, 500, 300)

        # Create main layout
        main_layout = QVBoxLayout()
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(main_layout)

        # Create the Thermal management group box
        thermal_box = QGroupBox("Thermal management")
        thermal_layout = QHBoxLayout()
        thermal_box.setLayout(thermal_layout)
        thermal_buttons = []
        for i in range(4):
            thermal_button = QRadioButton("Option {}".format(i+1))
            thermal_layout.addWidget(thermal_button)
            thermal_buttons.append(thermal_button)

        # Create the Battery configuration group box
        battery_box = QGroupBox("Battery configuration")
        battery_layout = QHBoxLayout()
        battery_box.setLayout(battery_layout)
        battery_buttons = []
        for i in range(5):
            battery_button = QRadioButton("Option {}".format(i+1))
            battery_layout.addWidget(battery_button)
            battery_buttons.append(battery_button)

        # Create the Battery sliders and labels
        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        self.slider_label_left = QLabel("0")
        self.slider_left = QSlider()
        self.slider_left.setOrientation(1)
        self.slider_left.setMinimum(0)
        self.slider_left.setMaximum(100)
        self.slider_left.setTickPosition(QSlider.TicksBothSides)
        self.slider_label_right = QLabel("100")
        self.slider_right = QSlider()
        self.slider_right.setOrientation(1)
        self.slider_right.setMinimum(0)
        self.slider_right.setMaximum(100)
        self.slider_right.setTickPosition(QSlider.TicksBothSides)
        slider_layout.addWidget(self.slider_label_left)
        slider_layout.addWidget(self.slider_left)
        slider_layout.addWidget(self.slider_label_right)
        slider_layout.addWidget(self.slider_right)

        # Create the Battery apply and cancel buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        apply_button = QPushButton("Apply")
        cancel_button = QPushButton("Cancel/Reload")
        button_layout.addWidget(apply_button)
        button_layout.addWidget(cancel_button)

        # Add all the widgets to the main layout
        main_layout.addWidget(thermal_box)
        main_layout.addWidget(battery_box)
        main_layout.addLayout(slider_layout)
        main_layout.addLayout(button_layout)

        # Create status bar and add status message
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # Connect slider signals to the slider labels
        self.slider_left.valueChanged.connect(lambda value: self.slider_label_left.setText(str(value)))
        self.slider_right.valueChanged.connect(lambda value: self.slider_label_right.setText(str(value)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
