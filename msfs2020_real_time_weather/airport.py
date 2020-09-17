import csv
import random
import urllib.request
from metar import Metar


class Airport:
    def __init__(self, icao_code_or_metar):
        # This is basically constructor overloading.
        if len(icao_code_or_metar) == 4:
            print(f'Downloading latest METAR for airport: {icao_code_or_metar}')
            icao_code = icao_code_or_metar
            self.info = _Info(icao_code)
            self.weather = _Weather(icao_code, self.info.altitude)
        elif len(icao_code_or_metar) > 4:
            print(f'Processing custom METAR: {icao_code_or_metar}')
            icao_code = icao_code_or_metar[:4]
            metar = icao_code_or_metar
            self.info = _Info(icao_code)
            self.weather = _Weather(icao_code, self.info.altitude, specific_metar=metar)
        else:
            print('Invalid ICAO code or METAR.')
            exit(1)


class _Info:
    def __init__(self, station_id):
        self.station_id = station_id
        self.info_dict = self._get_airport_info()
        self.airport_id = self.info_dict['Airport ID']
        self.name = self.info_dict['Name']
        self.city = self.info_dict['City']
        self.country = self.info_dict['Country']
        self.iata = self.info_dict['IATA']
        self.icao = self.info_dict['ICAO']
        self.latitude = self.info_dict['Latitude']
        self.longitude = self.info_dict['Longitude']
        self.altitude = self.info_dict['Altitude']
        self.timezone = self.info_dict['Timezone']
        self.dst = self.info_dict['DST']
        self.tz_database_time_zone = self.info_dict['Tz database time zone']
        self.type = self.info_dict['Type']
        self.source = self.info_dict['Source']

    def _get_airport_info(self):
        airport_file_header = ('Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude',
                               'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz database time zone', 'Type', 'Source')
        with open('msfs2020_real_time_weather/airports.dat', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, airport_file_header)
            for row in reader:
                if row['ICAO'] == self.station_id:
                    return row
            raise Exception(f'Airport "{self.station_id}" not found.')


class _Weather:
    def __init__(self, station_id, station_altitude, specific_metar=None):
        self.station_id = station_id
        self.station_altitude = station_altitude
        try:
            print('Parsing METAR.')
            if specific_metar is None:
                self.parsed_metar = Metar.Metar(self._download_metar())
            else:
                self.parsed_metar = Metar.Metar(specific_metar)
        except Exception as exp:
            print(exp)
        else:
            print('Metar successfully parsed.')
        self.code = self._get_metar_code()
        self.pressure = self._get_pressure()
        self.msl_temperature = self._get_msl_temperature()
        self.wind_dir = self._get_wind_dir()
        self.wind_speed = self._get_wind_speed()
        self.cloud_layers = self._get_cloud_layers()

    def _download_metar(self):
        url = f'https://tgftp.nws.noaa.gov/data/observations/metar/stations/{self.station_id}.TXT'
        try:
            with urllib.request.urlopen(url) as f:
                extracted_metar = f.read().decode('utf-8')
                extracted_metar = extracted_metar.split('\n', 1)[1]
                return extracted_metar
        except urllib.error.URLError as e:
            print(e.reason)

    def _get_metar_code(self):
        return self.parsed_metar.code

    def _get_pressure(self):
        return f'{round(self.parsed_metar.press.value("hpa") * 100, 3):.3f}' if self.parsed_metar.press else None

    def _get_msl_temperature(self):
        airport_altitude = int(self.station_altitude)
        return str(round(self.parsed_metar.temp.value('k') + ((airport_altitude / 1000) * 2), 3)) \
            if self.parsed_metar.temp else None

    def _get_wind_dir(self):
        # When wind is variable, a random direction will be set.
        random_direction = f'{random.randint(0, 359)}.000'
        return str(round(self.parsed_metar.wind_dir.value(), 3)) if self.parsed_metar.wind_dir else random_direction

    def _get_wind_speed(self):
        return str(round(self.parsed_metar.wind_speed.value('KT'), 3)) if self.parsed_metar.wind_speed else None

    # TODO Airports with no cloud data won't get clouds in-game.
    # TODO Airports that have the first layer as OVC and no other layers, won't have clouds above said OVC layer.
    def _get_cloud_layers(self):
        parsed_sky = self.parsed_metar.sky
        exportable_cloud_layers = list()

        def _fill_exportable_cloud_layers(cloud_layers, num_of_layers):
            for _ in range(num_of_layers):
                cloud_layers.append(dict(
                    CloudLayerDensity='0.000',
                    CloudLayerAltitudeBot='5000.000',
                    CloudLayerAltitudeTop='5000.000',
                    # TODO Maybe randomize the scattering?
                    CloudLayerScattering='1.000'
                ))
            return cloud_layers

        exportable_cloud_layers = _fill_exportable_cloud_layers(exportable_cloud_layers, 3)

        def _set_cloud_layer_density(parsed_cloud_layer, exportable_cloud_layer):
            parsed_cloud_cover = parsed_cloud_layer[0]
            if parsed_cloud_cover == 'CLR' or parsed_cloud_cover == 'NCD':
                cloud_layer_density = '0.000'
            elif parsed_cloud_cover == 'NSC':
                cloud_layer_density = f'{round(random.uniform(0.001, 0.124), 3):.3f}'
            elif parsed_cloud_cover == 'FEW':
                cloud_layer_density = f'{round(random.uniform(0.125, 0.3124), 3):.3f}'
            elif parsed_cloud_cover == 'SCT':
                cloud_layer_density = f'{round(random.uniform(0.3125, 0.5624), 3):.3f}'
            elif parsed_cloud_cover == 'BKN':
                cloud_layer_density = f'{round(random.uniform(0.5625, 0.999), 3):.3f}'
            elif parsed_cloud_cover == 'OVC':
                cloud_layer_density = '1.000'
            else:
                cloud_layer_density = '0.000'
            exportable_cloud_layer['CloudLayerDensity'] = cloud_layer_density
            return exportable_cloud_layer

        def _get_cloud_layer_altitude_bot(parsed_cloud_layer, exportable_cloud_layer):
            if parsed_cloud_layer[1] is None:
                return exportable_cloud_layer
            parsed_cloud_layer_altitude_bot = f'{round(parsed_cloud_layer[1].value("M"), 3):.3f}'
            exportable_cloud_layer['CloudLayerAltitudeBot'] = parsed_cloud_layer_altitude_bot
            return exportable_cloud_layer

        def _get_cloud_layer_altitude_top(parsed_cloud_layer, exportable_cloud_layer):
            if parsed_cloud_layer[1] is None:
                return exportable_cloud_layer
            cloud_layer_altitude_bot = float(exportable_cloud_layer['CloudLayerAltitudeBot'])
            parsed_cloud_type = parsed_cloud_layer[2]
            # From what I've gathered, clouds usually get thinner if their base is above 5000m AGL.
            # These cloud thickness values have not been properly tested yet.
            if cloud_layer_altitude_bot < 5000:
                if parsed_cloud_type == 'TCU':
                    parsed_cloud_layer_altitude_top = random.randint(2000, 3000)
                elif parsed_cloud_type == 'CB':
                    parsed_cloud_layer_altitude_top = random.randint(3000, 6000)
                else:
                    parsed_cloud_layer_altitude_top = random.randint(750, 1250)
            else:
                # TODO this is too simple. should be proportionate to height
                parsed_cloud_layer_altitude_top = random.randint(250, 750)

            exportable_cloud_layer['CloudLayerAltitudeTop'] = \
                f'{round(cloud_layer_altitude_bot + parsed_cloud_layer_altitude_top):.3f}'
            return exportable_cloud_layer

        exportable_cloud_layers = list(map(_set_cloud_layer_density, parsed_sky, exportable_cloud_layers))
        exportable_cloud_layers = list(map(_get_cloud_layer_altitude_bot, parsed_sky, exportable_cloud_layers))
        exportable_cloud_layers = list(map(_get_cloud_layer_altitude_top, parsed_sky, exportable_cloud_layers))

        missing_layers = 3 - len(exportable_cloud_layers)
        exportable_cloud_layers = _fill_exportable_cloud_layers(exportable_cloud_layers, missing_layers)

        return exportable_cloud_layers
