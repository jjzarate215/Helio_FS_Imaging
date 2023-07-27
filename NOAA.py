
from sunpy.net import Fido, attrs as a
from sunpy.io.special import srs
import numpy as np

day = '2022-12-10'  # Specify the date of interest

# Search for SRS data for the specified date using Fido
srs_search = Fido.search(a.Time(day, day), a.Instrument.srs_table)

# Fetch the downloaded SRS data and store it in the current directory
downloaded_srs = Fido.fetch(srs_search, path='./{file}')

# Read the downloaded SRS data using the srs module and store it in a variable
srs_table = srs.read_srs(downloaded_srs[0])

# Filter the SRS table to include only rows with ID 'I' or 'IA'
# I.  Regions with Sunspots
# IA. H-alpha Plages without Spots
srs_table = srs_table[np.logical_or(srs_table['ID'] == 'I', srs_table['ID'] == 'IA')]






