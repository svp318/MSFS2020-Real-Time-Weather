import os
import sys
from io import StringIO

from .airport import Airport
from .msfs_xml import MsfsXML

from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication


# Hacky but fast way of capturing print statements from other modules
# Will refactor this in the future
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


class DialogGUI(QDialog):
    def __init__(self):
        super(DialogGUI, self).__init__()
        loadUi('msfs2020_real_time_weather/window.ui', self)
        self.Return = 0

        self.create_preset_button.clicked.connect(self.create_preset)

    def print_to_output(self, output_text):
        self.result_output_text_browser.append(output_text)

    @pyqtSlot()
    def create_preset(self):

        # Set the airport ICAO code here.
        airport_icao_code = self.id_input.text()

        # This will use the test file in this folder.
        # Set to false to use the file in the MSFS Presets folder.
        using_test_file = False

        with Capturing() as output:
            airport = Airport(airport_icao_code)
        for line in output:
            self.print_to_output(line)

        preset_file_name = f'{airport.info.station_id}.WPR'
        if using_test_file:
            preset_file_location = preset_file_name
        else:
            preset_file_location = os.getenv('APPDATA') + \
                                   fr'\Microsoft Flight Simulator\Weather\Presets\{preset_file_name} '

        with Capturing() as output:
            weather_preset = MsfsXML(preset_file_location)
        for line in output:
            self.print_to_output(line)

        with Capturing() as output:
            weather_preset.set_real_weather(airport)
        for line in output:
            self.print_to_output(line)

        with Capturing() as output:
            weather_preset.save_file(airport)
        for line in output:
            self.print_to_output(line)


def run():
    app = QApplication(sys.argv)
    window = DialogGUI()
    window.show()
    sys.exit(app.exec_())
