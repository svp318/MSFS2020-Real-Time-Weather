# Original Author: Simon Vega - 2020
# Distributed under the terms of the GNU GPLv3 License.
import asyncio
import os
import sys
import threading

from io import StringIO

from .airport import Airport
from .msfs_xml import MsfsXML
from .dialog_GUI import DialogGUI
from .messages import Messages as M

from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication


# Hacky but fast way of capturing print statements from other modules
# Will refactor this in the future
# class Capturing(list):
#     def __enter__(self):
#         self._stdout = sys.stdout
#         sys.stdout = self._stringio = StringIO()
#         return self
#
#     def __exit__(self, *args):
#         self.extend(self._stringio.getvalue().splitlines())
#         del self._stringio    # free up some memory
#         sys.stdout = self._stdout


@pyqtSlot()
def create_preset(window):

    # Set the airport ICAO code here.
    AIRPORT_ICAO_CODE = window.id_input.text()

    # This will use the test file in this folder.
    # Set to false to use the file in the MSFS Presets folder.
    USING_TEST_FILE = False

    airport = Airport(AIRPORT_ICAO_CODE)

    # TODO Select Steam/Windows Store/Custom Folder location for the preset file
    preset_file_name = f'{airport.info.station_id}.WPR'
    if USING_TEST_FILE:
        PRESET_FILE_LOCATION = preset_file_name
    else:
        PRESET_FILE_LOCATION = os.getenv('APPDATA') + \
                               fr'\Microsoft Flight Simulator\Weather\Presets\{preset_file_name}'

    weather_preset = MsfsXML(PRESET_FILE_LOCATION)

    weather_preset.set_real_weather(airport)

    weather_preset.save_file(airport)


async def thread_test(text):
    while True:
        M.send_message(text)
        await asyncio.sleep(1)


async def thread_test2():
    print('here')
    M.send_message('plPA')


def run():
    app = QApplication(sys.argv)
    window = DialogGUI()
    window.create_preset_button.clicked.connect(lambda: create_preset(window))
    # threading.Thread(
    #     target=window.create_preset_button.clicked.connect,
    #     args=(thread_test2,)
    # ).start()
    window.show()
    # threading.Thread(target=asyncio.run, args=(thread_test('palapaa'),)).start()
    sys.exit(app.exec_())
