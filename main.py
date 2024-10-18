import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel, QLineEdit, QFileDialog, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('SubliminalHack GUI')
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #f0f0f0;
                font-size: 14px;
            }
            QPushButton {
                background-color: #444;
                color: #f0f0f0;
                border: none;
                padding: 8px;
            }
            QPushButton:disabled {
                background-color: #111;
                color: #c0c0c0;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #888;
            }
            QSlider::groove:horizontal {
                background-color: #444;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: #888;
                width: 14px;
                height: 14px;
                border-radius: 7px;
                margin: -3px 0;
            }
            QLineEdit {
                background-color: #333;
                border: 1px solid #555;
                color: #f0f0f0;
                padding: 4px;
            }
            QLabel {
                color: #f0f0f0;
            }
        """)

        self.layout = QVBoxLayout()

        self.add_file_picker_with_description('Choose File')

        self.add_slider_with_description('Volume', 50)
        self.add_slider_with_description('Delay (ms)', 2000)

        self.play_button = QPushButton('Play', self)
        self.stop_button = QPushButton('Stop', self)

        self.stop_button.setEnabled(False)

        self.play_button.clicked.connect(self.play)
        self.stop_button.clicked.connect(self.stop)

        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)

        self.player = QMediaPlayer()
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_audio)

    def add_slider_with_description(self, description, value=50):
        label = QLabel(description, self)
        slider = QSlider(Qt.Horizontal, self)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(value)

        slider.valueChanged.connect(self.handle_slider_change)

        if description == 'Volume':
            self.volume_slider = slider
        elif description == 'Delay (ms)':
            self.delay_slider = slider

        self.layout.addWidget(label)
        self.layout.addWidget(slider)

    def handle_slider_change(self, value):
        if self.sender() == self.volume_slider:
            self.player.setVolume(value)
        elif self.sender() == self.delay_slider:
            self.timer.setInterval(value)

    def add_file_picker_with_description(self, description):
        label = QLabel(description, self)
        self.layout.addWidget(label)

        h_layout = QHBoxLayout()

        self.file_path = QLineEdit(self)
        h_layout.addWidget(self.file_path)

        browse_button = QPushButton('Browse', self)
        browse_button.clicked.connect(self.open_file_dialog)
        h_layout.addWidget(browse_button)

        self.layout.addLayout(h_layout)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Audio Files (*.mp3 *.wav)')
        if file_name:
            self.file_path.setText(file_name)

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec_()

    def play_audio(self):
        if self.player.media() is not None:
            self.player.play()

    def play(self):
        file_path = self.file_path.text()

        if not file_path:
            self.show_error_message("No file path provided!")
            return

        if not os.path.exists(file_path):
            self.show_error_message("File not found!")
            return

        media_url = QUrl.fromLocalFile(file_path)

        if media_url.isValid():
            self.player.setMedia(QMediaContent(media_url))
        else:
            self.show_error_message("Invalid file path.")
            return

        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.timer.start(self.delay_slider.value() * 10)

    def stop(self):
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.timer.stop()
        self.player.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
