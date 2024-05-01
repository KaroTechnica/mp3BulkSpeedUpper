import sys
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from PyQt6.QtCore import QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QDesktopServices

class ConversionThread(QThread):
    conversion_done = pyqtSignal()

    def __init__(self, input_files):
        super().__init__()
        self.input_files = input_files

    def run(self):
        output_folder = "C:/Users/Administrateur/Downloads/AudioSpeedUpper"
        os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist
        for input_file in self.input_files:
            output_file = os.path.join(output_folder, os.path.basename(input_file))  # Use input file's name for output
            subprocess.run(['ffmpeg', '-i', input_file, '-filter:a', 'atempo=1.84', output_file])
            print(f"Conversion completed for {input_file}")
        print("All files converted.")
        self.conversion_done.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MP3 Converter")
        self.setGeometry(100, 100, 400, 250)

        self.btn_select_file = QPushButton("Select Input File(s)", self)
        self.btn_select_file.setGeometry(50, 50, 150, 30)
        self.btn_select_file.clicked.connect(self.select_input_files)

        self.btn_convert = QPushButton("Convert", self)
        self.btn_convert.setGeometry(220, 50, 150, 30)
        self.btn_convert.clicked.connect(self.convert_files)

        self.btn_restart = QPushButton("Restart Program", self)
        self.btn_restart.setGeometry(130, 150, 150, 30)
        self.btn_restart.clicked.connect(self.restart_program)

        self.selected_files_label = QLabel("", self)
        self.selected_files_label.setGeometry(50, 100, 320, 30)

        self.selected_files = []

        # Connect conversion_done signal to handle_conversion_done method
        self.conversion_thread = ConversionThread([])
        self.conversion_thread.conversion_done.connect(self.handle_conversion_done)

    def select_input_files(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("MP3 files (*.mp3)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)  # Allow selecting multiple existing files
        if file_dialog.exec():
            self.selected_files = file_dialog.selectedFiles()
            num_files = len(self.selected_files)
            self.selected_files_label.setText(f"{num_files} file(s) selected")

    def convert_files(self):
        if self.selected_files:
            self.btn_convert.setEnabled(False)  # Disable the convert button during conversion
            self.conversion_thread.input_files = self.selected_files  # Update input files
            self.conversion_thread.start()
        else:
            print("Please select at least one input file.")

    def handle_conversion_done(self):
        self.btn_convert.setEnabled(True)  # Re-enable the convert button
        print("Conversion completed for all selected files.")
        output_folder = "C:/Users/Administrateur/Downloads/AudioSpeedUpper"
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(output_folder))  # Open the output folder
        except Exception as e:
            print(f"Error opening folder: {e}")

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
