# Jon Zarate
# Shea A. Hess Webber
# Milo Buitrago-Casas
# Exploring the Unseen Sun
# Date Created: 06-21-2023
#
#

import sunpy
from sunpy.net import jsoc
from sunpy.net import attrs as a 

jsoc_client = jsoc.JSOCClient()
response = jsoc_client.search(
    a.Time("2023.05.01_00:00:00_TAI", "2023.05.31_12:00:00_TAI"),
    a.jsoc.Series("hmi.td_fsi_12h"),
    a.jsoc.Notify("jjzarate215@gmail.com")
    )
print(response)


