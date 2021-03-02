# Original Author: Simon Vega - 2020
# Distributed under the terms of the GNU GPLv3 License.

import xml.etree.ElementTree as ET
from .messages import Messages as M


# TODO Add an option to save a departure airport and a destination airport
class MsfsXML:
    def __init__(self, preset_file_location):
        self.preset_file_location = preset_file_location
        self.template_file = 'msfs2020_real_time_weather/template.xml'
        self.tree = ET.parse(self.template_file)
        self.root = self.tree.getroot()
        self.weather_preset = self.root.find('WeatherPreset.Preset')
        self.ground_wind_layer = self._get_ground_wind_layer()

    def _get_ground_wind_layer(self):
        wind_layers = self.weather_preset.findall('WindLayer')
        for wind_layer in wind_layers:
            wind_layer_altitude = float(wind_layer.find('WindLayerAltitude').attrib['Value'])
            if wind_layer_altitude == 0:
                return wind_layer
        M.send_message('Ground wind layer not found.')

    def _set_preset_name(self, station_id):
        self.weather_preset.find('Name').text = station_id

    def _set_value(self, weather_preset_node, value):
        if value is not None:
            weather_preset_node.set('Value', value)
        else:
            M.send_message(f'No information in METAR for {weather_preset_node.tag}. Will not update this tag.')

    def _set_pressure(self, value):
        tag = self.weather_preset.find('MSLPressure')
        self._set_value(tag, value)

    def _set_msl_temperature(self, value):
        tag = self.weather_preset.find('MSLTemperature')
        value = value
        self._set_value(tag, value)

    def _set_wind_dir(self, value):
        tag = self.ground_wind_layer.find('WindLayerAngle')
        self._set_value(tag, value)

    def _set_wind_speed(self, value):
        tag = self.ground_wind_layer.find('WindLayerSpeed')
        self._set_value(tag, value)

    # TODO Set GustWave information

    def _set_cloud_layers(self, value):
        cloud_layers = self.weather_preset.findall('CloudLayer')
        for i, cloud_layer in enumerate(cloud_layers):
            cloud_layer_density = cloud_layer.find('CloudLayerDensity')
            cloud_layer_altitude_bot = cloud_layer.find('CloudLayerAltitudeBot')
            cloud_layer_altitude_top = cloud_layer.find('CloudLayerAltitudeTop')
            cloud_layer_scattering = cloud_layer.find('CloudLayerScattering')
            self._set_value(cloud_layer_density, value[i]['CloudLayerDensity'])
            self._set_value(cloud_layer_altitude_bot, value[i]['CloudLayerAltitudeBot'])
            self._set_value(cloud_layer_altitude_top, value[i]['CloudLayerAltitudeTop'])
            self._set_value(cloud_layer_scattering, value[i]['CloudLayerScattering'])

    # TODO Precipitation

    # TODO Lightning

    def set_real_weather(self, airport):
        self._set_preset_name(airport.info.station_id)
        self._set_pressure(airport.weather.pressure)
        self._set_msl_temperature(airport.weather.msl_temperature)
        self._set_wind_dir(airport.weather.wind_dir)
        self._set_wind_speed(airport.weather.wind_speed)
        self._set_cloud_layers(airport.weather.cloud_layers)

    def save_file(self, airport):
        try:
            self.tree.write(self.preset_file_location, encoding='UTF-8', xml_declaration=True)
        except FileNotFoundError:
            M.send_message(f'Error, could not create or update weather preset at {self.preset_file_location}.')
        except Exception as exp:
            M.send_message(exp)
        else:
            M.send_message(f'Weather preset successfully created at {self.preset_file_location}')
            M.send_message('The following METAR was used to update it:')
            M.send_message(airport.weather.code)
