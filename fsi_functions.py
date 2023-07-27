# Jon Zarate
# Shea A. Hess Webber
# Milo Buitrago-Casas
# Exploring the Unseen Sun
# Date Created: 07-21-2023


""" The following defines functions that can be used to download far-side helioseismic images (fsi) 
from the jsoc server and extract data from fsi for data visualization purposes  """


from sunpy.net import Fido
from sunpy.net import attrs as a

import os
from astropy.io import fits
from datetime import datetime

from scipy import ndimage
import numpy as np


def hmi_downloader(jsoc_series, jsoc_email, first_rec, last_rec, dwnld_dir):
    
     """ downloads time-distance fsi from jsoc server, parameters include  """
    
     query = Fido.search(a.Time(first_rec, last_rec), a.jsoc.Series(jsoc_series),a.jsoc.Notify(jsoc_email))
     
     dwnld = Fido.fetch(query, path = dwnld_dir, progress = True, overwrite = False)


##################################### extracts data from time-distance helioseismic far-side images ###########
def extract_fsi_data(dwnld_dir):
    """ extracts data from """

    fsi_images = []
    fsi_data =[]
    fsi_headers = []
    date_t = []
    mean_val = []
    median_val = []

    for fits_file in os.listdir(dwnld_dir):
        if os.path.isfile(os.path.join(dwnld_dir, fits_file)):
            fsi_images.append(fits_file)

            hdu = fits.open(os.path.join(dwnld_dir, fits_file))
            image_data = hdu[0].data
            image_header = hdu[0].header['DATE-OBS']
            average_value = hdu[0].header['DATAMEAN']
            median_value = hdu[0].header['DATAMEDN']
            hdu.close()

            fsi_data.append(image_data)
            fsi_headers.append(image_header)
            mean_val.append(average_value)
            median_val.append(median_value)
    
    # Converts header string dates to datetime object and then to an alternatively formatted string output
    for i in fsi_headers:
          date_t.append((datetime.strptime(i,'%Y-%m-%dT%H:%M:%S.%f').strftime('%b %d, %Y %I:%M %p')))
    
    return {'images': fsi_images, 'image datum': fsi_data, 
             'image headers': date_t, 'image mean pix val': mean_val, 
             'image median pix val': median_val}


############################# creates mask and counts dark regions (sunspots) #####################
def create_mask(image_data, image_mean_pix_val):
     
     bool_mask = []
     mask_data = []
     mask_data_mean = []
     dark_regions = []

     for i in range(len(image_data)):
        mask = image_data[i] < image_mean_pix_val[i] - image_data[i].std() * 2.5
        filtered_data = image_data[i] * mask
    
        new_filtered_data = np.where(filtered_data == 0, np.nan, filtered_data)
        filtered_data_mean = np.nanmean(new_filtered_data)

        labels, n = ndimage.label(mask)

        bool_mask.append(mask)
        mask_data.append(filtered_data)
        mask_data_mean.append(filtered_data_mean)
        dark_regions.append(n)

     return{'boolean mask': bool_mask, 'mask data': mask_data,
            'mask data mean': mask_data_mean, 'dark regions': dark_regions}





