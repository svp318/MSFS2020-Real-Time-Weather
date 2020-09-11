import os
from airport import Airport
from msfs_xml import MsfsXML


if __name__ == '__main__':

    preset_file_location = os.getenv('APPDATA') + r'\Microsoft Flight Simulator\Weather\Presets\CustomSky.WPR'
    print(f'Looking for weather preset at {preset_file_location}')
    airport = Airport('SEQM')
    weather_preset = None

    try:
        weather_preset = MsfsXML(preset_file_location)
    except FileNotFoundError:
        print('Error, weather preset not found.\n'
              'You must first create a custom preset in-game called Custom Sky.\n')
        exit(1)
    except Exception as exp:
        print(exp)
    else:
        print(f'Weather preset successfully found.')

    weather_preset.set_real_weather(airport)

    try:
        print('Updating weather preset.')
        weather_preset.save_file()
    except Exception as exp:
        print(f'Error, could not update weather preset.\n{exp}')
    else:
        print('Weather preset successfully updated with the following METAR:')
        print(airport.weather.code)
