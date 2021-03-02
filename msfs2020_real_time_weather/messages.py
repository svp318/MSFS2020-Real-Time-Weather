# Original Author: Simon Vega - 2020
# Distributed under the terms of the GNU GPLv3 License.

from .dialog_GUI import DialogGUI


class Messages:
    @staticmethod
    def send_message(text):
        DialogGUI.print_to_output(text)
