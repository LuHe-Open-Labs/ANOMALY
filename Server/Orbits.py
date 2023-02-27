
# Plot planets orbits with astropy
# Distances in Unity = x in mKm (millions of km) * 10

from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric

def orbit(time, celestial):
    # Use astropy to get the position of the celestial body
    # at the given time
    # celestial is a string with the name of the celestial body
    # time is a string with the date and time in ISO format
    # Return the position of the celestial body in Unity units
    # (millions of km * 10)
    with solar_system_ephemeris.set('jpl'):
        pos = get_body_barycentric(celestial, Time(time)).xyz.value * 10
    return pos
