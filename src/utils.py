from datetime import datetime

class Utils:
    def get_datetime_from_str(string):
        splitted = string.split()
        date = [int(i) for i in splitted[0].split('.')]
        time = [int(i) for i in splitted[1].split(':')]
        dt = datetime(date[2], date[1], date[0], time[0], time[1])
        return dt
    
    def get_coords_from_str(string):
        coords_str = string[1:-1].split(', ')
        coords = [float(coord) for coord in coords_str]
        return coords

