import os
from airport import Airport
from msfs_xml import MsfsXML


if __name__ == '__main__':

    # Set the airport ICAO code here.
    airport_icao_code = 'KORD'

    # This will use the test file in this folder.
    # Set to false to use the file in the MSFS Presets folder.
    using_test_file = False

    airport = Airport(airport_icao_code)
    weather_preset = None

    preset_file_name = f'{airport.info.station_id}.WPR'
    if using_test_file:
        preset_file_location = preset_file_name
    else:
        preset_file_location = os.getenv('APPDATA') + fr'\Microsoft Flight Simulator\Weather\Presets\{preset_file_name}'

    weather_preset = MsfsXML(preset_file_location)
    weather_preset.set_real_weather(airport)
    weather_preset.save_file(airport)
