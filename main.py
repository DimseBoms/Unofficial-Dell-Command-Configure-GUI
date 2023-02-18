import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QComboBox, QRadioButton, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Application')
        
        # Create a status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # Create the first set of radio buttons
        self.radio_button1a = QRadioButton('Option 1A')
        self.radio_button1b = QRadioButton('Option 1B')
        self.radio_group1 = QGroupBox('First Set of Radio Buttons')
        layout1 = QVBoxLayout()
        layout1.addWidget(self.radio_button1a)
        layout1.addWidget(self.radio_button1b)
        self.radio_group1.setLayout(layout1)
        
        # Create the second set of radio buttons
        self.radio_button2a = QRadioButton('Option 2A')
        self.radio_button2b = QRadioButton('Option 2B')
        self.radio_group2 = QGroupBox('Second Set of Radio Buttons')
        layout2 = QVBoxLayout()
        layout2.addWidget(self.radio_button2a)
        layout2.addWidget(self.radio_button2b)
        self.radio_group2.setLayout(layout2)
        
        # Create the first drop-down
        self.combo_box1 = QComboBox()
        self.combo_box1.addItem('Option 1')
        self.combo_box1.addItem('Option 2')
        self.combo_box1.addItem('Option 3')
        label1 = QLabel('First Drop-down:')
        layout3 = QHBoxLayout()
        layout3.addWidget(label1)
        layout3.addWidget(self.combo_box1)
        
        # Create the second drop-down
        self.combo_box2 = QComboBox()
        self.combo_box2.addItem('Option A')
        self.combo_box2.addItem('Option B')
        label2 = QLabel('Second Drop-down:')
        layout4 = QHBoxLayout()
        layout4.addWidget(label2)
        layout4.addWidget(self.combo_box2)
        
        # Create the confirm and cancel buttons
        self.confirm_button = QPushButton('Confirm')
        self.cancel_button = QPushButton('Cancel')
        layout5 = QHBoxLayout()
        layout5.addWidget(self.confirm_button)
        layout5.addWidget(self.cancel_button)
        
        # Create the main layout and add the components
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.radio_group1)
        main_layout.addWidget(self.radio_group2)
        main_layout.addLayout(layout3)
        main_layout.addLayout(layout4)
        main_layout.addLayout(layout5)
        
        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Connect signals to slots
        self.confirm_button.clicked.connect(self.confirm_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        
    def confirm_button_clicked(self):
        message = f'Radio buttons selected: {self.radio_group1.title()} = '
        if self.radio_button1a.isChecked():
            message += 'Option 1A, '
        elif self.radio_button1b.isChecked():
            message += 'Option 1B, '
        message += f'{self.radio_group2.title()} = '
        if self.radio_button2a.isChecked():
            message += 'Option 2A, '
        elif self.radio_button2b.isChecked():
            message += 'Option 2B, '
        message += f'Drop-downs selected: {self.combo_box1.currentText()}, {self.combo_box2.currentText()}'
        self.status_bar.showMessage

    def cancel_button_clicked(self):
        self.status_bar.showMessage('Cancelled')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
