import xml.etree.ElementTree as ET


# TODO Get XML from a template file in the project directory
# TODO Add an option to save a departure airport and a destination airport
class MsfsXML:
    def __init__(self, preset_file_location):
        self.preset_file_location = preset_file_location
        self.tree = ET.parse(self.preset_file_location)
        self.root = self.tree.getroot()
        self.weather_preset = self.root.find('WeatherPreset.Preset')
        self.ground_wind_layer = self._get_ground_wind_layer()

    def _get_ground_wind_layer(self):
        wind_layers = self.weather_preset.findall('WindLayer')
        for wind_layer in wind_layers:
            wind_layer_altitude = float(wind_layer.find('WindLayerAltitude').attrib['Value'])
            if wind_layer_altitude == 0:
                return wind_layer
        print('Ground wind layer not found.')

    def _set_value(self, weather_preset_node, value):
        if value is not None:
            weather_preset_node.set('Value', value)
        else:
            print(f'No information in METAR for {weather_preset_node.tag}. Will not update this tag.')

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

    # TODO Cloud Layers

    # TODO Precipitation

    # TODO Lightning

    def set_real_weather(self, airport):
        self._set_pressure(airport.weather.pressure)
        self._set_msl_temperature(airport.weather.msl_temperature)
        self._set_wind_dir(airport.weather.wind_dir)
        self._set_wind_speed(airport.weather.wind_speed)

    def save_file(self):
        self.tree.write(self.preset_file_location, encoding='UTF-8', xml_declaration=True)
