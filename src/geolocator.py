from geopy.geocoders import Nominatim
import math
# import pyproj

from utils import Utils

class Geolocator:
    """Determines the location by coordinates"""
    __geolocator = Nominatim()
    
    def get_state(coords):
        """Finds the city/state by coordinates"""
        coords_str = '{}, {}'.format(coords[0], coords[1])
        location = Geolocator.__geolocator.reverse(coords_str, exactly_one=True)
        try:
            address = location.raw['address']
        except KeyError:
            return None
        state = address.get('state', '')
        return state
    
    def merc_to_lat_long(coords):
        # Using pyproj also gives the wrong result
        # p = pyproj.Proj("+proj=merc +ellps=WGS84")
        # coords[0], coords[1] = p(coords[0], coords[1], inverse=True)
        coords[1] = math.degrees(2*math.atan(math.tanh(0.5*math.radians(coords[1]))))
        return coords

    def get_lat_long_from_merc(gps_str):
        merc = Utils.get_coords_from_str(gps_str)
        lat_long = Geolocator.merc_to_lat_long(merc)
        return lat_long

class MoscowIndentifier:
    """Indentify whether the coordinates point to Moscow"""
    def is_Moscow(gps):
        """Compares coordinates in Mercator with the coordinates of Moscow"""
        if gps == 'None':
            return False
        coords = Geolocator.get_lat_long_from_merc(gps)
        if not MoscowIndentifier.is_Moscow_simple(coords):
            return False
        return Geolocator.get_state(coords) == 'Москва'
    
    def is_Moscow_simple(coords):
        """Compares coordinates with approximate coordinates of Moscow"""
        x = coords[0]
        y = coords[1]
        return x > 55 and x < 56.1 and y > 36.7 and y < 38
