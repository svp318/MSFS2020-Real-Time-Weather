import csv
import random
import urllib.request
from metar import Metar


class Airport:
    def __init__(self, station_id):
        self.station_id = station_id
        self.info = _Info(self.station_id)
        self.weather = _Weather(self.station_id, self.info.altitude)


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
        with open('airports.dat', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, airport_file_header)
            for row in reader:
                if row['ICAO'] == self.station_id:
                    return row
            raise Exception(f'Airport "{self.station_id}" not found.')


class _Weather:
    def __init__(self, station_id, station_altitude):
        self.station_id = station_id
        self.station_altitude = station_altitude
        self.parsed_metar = Metar.Metar(self._download_metar())
        self.code = self._get_metar_code()
        self.pressure = self._get_pressure()
        self.msl_temperature = self._get_msl_temperature()
        self.wind_dir = self._get_wind_dir()
        self.wind_speed = self._get_wind_speed()

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
