# Original Author: Simon Vega - 2020
# Distributed under the terms of the GNU GPLv3 License.

from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication


class DialogGUI(QDialog):

    def __init__(self):
        super(DialogGUI, self).__init__()
        loadUi('msfs2020_real_time_weather/window.ui', self)
        self.Return = 0
        DialogGUI.output_text_box = self.result_output_text_browser
        self.header_info_label.setOpenExternalLinks(True)

    @staticmethod
    def print_to_output(output_text):
        DialogGUI.output_text_box.append(output_text)
