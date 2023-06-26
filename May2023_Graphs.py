# Jon Zarate
# Shea A. Hess Webber
# Milo Buitrago-Casas
# Exploring the Unseen Sun
# Date Created: 06-21-2023
#
#

import sunpy
from sunpy.net import Fido
from sunpy.net import attrs as a

jsoc_email = "jjzarate215@berkeley.edu"


query = Fido.search(
    a.Time('2023.05.01_00:00:00_TAI', '2023.05.31_12:00:00_TAI'),
    a.jsoc.Series('hmi.td_fsi_12h'),
    a.jsoc.Notify(jsoc_email)
)

print(query)
directory = 'C:\\Users\\Jjzar\\OneDrive\\Documents\\ASSURE\\ASSURE 2023\\Exploring the Unseen Sun\\Far-SideImagingData\\May2023'
download_fsi = Fido.fetch(query, path = directory)

#########################################################################




