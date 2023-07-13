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

import os
from astropy.io import fits
from datetime import datetime

######################################## downloads JSOC time-distance helioseismic far-side images ###############################################

def hmi_downloader(jsoc_series, jsoc_email, first_rec, last_rec, dwnld_dir):
     
     """ downloads time-distance helioseismic far-side images
       from jsoc server and extracts data """
     
     query = Fido.search(
    a.Time(first_rec, last_rec),
    a.jsoc.Series(jsoc_series),
    a.jsoc.Notify(jsoc_email) 
    )
     
     dwnld = Fido.fetch(query, path = dwnld_dir)

     fsi_images = []
     fsi_data =[]
     fsi_headers = []
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
     date_t = []
     for i in fsi_headers:
          date_t.append((datetime.strptime(i,'%Y-%m-%dT%H:%M:%S.%f').strftime('%b %d')))
    
     return {'images': fsi_images, 'image datum': fsi_data, 
             'image headers': date_t, 'image mean pix_val': mean_val, 
             'image median pix_val': median_val}


series = 'hmi.td_fsi_12h'
email = 'jjzarate215@berkeley.edu'
f_rec = '2023.05.01_00:00:00_TAI'
l_rec = '2023.05.31_12:00:00_TAI'
fsi_directory = 'C:\\Users\\Jjzar\\OneDrive\\Documents\\ASSURE\\ASSURE 2023\\Exploring the Unseen Sun\\Far-SideImagingData\\May2023'


results = hmi_downloader(series, email, f_rec, l_rec, fsi_directory)



######################################################### extracts data from images ###################################################


import matplotlib.pyplot as plt
import sunpy.map
from scipy import ndimage
import numpy as np

## Added two new imports here
from matplotlib import ticker



# ## This line is useful if you want to ultimately plot more than one plot in the same figure
# fig, axs = plt.subplots(1, 1, figsize=(8, 5), layout='constrained')

# axs.scatter(dt, avg_may, color = 'red') #note the new x-axis variable!
# plt.xlabel('Observed Time')
# plt.ylabel('Average Pixel Value')
# plt.title('Average Phase Shift (May 2023)')

# axs.tick_params(axis='x', rotation=55)
# axs.xaxis.set_major_locator(ticker.MultipleLocator(7)) # right now I have this set to only show one date per week (major, with tick labels)
# axs.xaxis.set_minor_locator(ticker.MultipleLocator(1)) # this is set to show one tick per day (minor, no labels)

# plt.show()


# plt.scatter(fsi_headers, med_may, color = 'red')
# plt.xlabel('Observed Time')
# plt.ylabel('Median Pixel Value')
# plt.title('Untitled')
# plt.show()


######################################################## creates mask #######################################################################
import astropy.units as u

#mask = data < data.mean() - data.std() * 2.5
#data_masked = data * mask

mask = []
data_masked = []
sunspots_num = []



for i in range(len(results['image datum'])):
    m = results['image datum'][i] < results['image mean pix_val'][i] - results['image datum'][i].std() * 2.5
    d_m = results['image datum'][i] * m
    #mean
    labels, n = ndimage.label(m)

    mask.append(m)
    data_masked.append(d_m)
    sunspots_num.append(n)

print(sunspots_num)
print(len(sunspots_num))


# for i in range(len(fsi_data)):
#     m = fsi_data[i] < avg_may[i] - fsi_data[i].std() * 2.5
#     d_m = fsi_data[i] * m
#     #mean
#     labels, n = ndimage.label(m)

#     mask.append(m)
#     data_masked.append(d_m)
#     sunspots_num.append(n)

# print(sunspots_num)
# print(len(sunspots_num))


#improve on the future
labeled_array, num_features = ndimage.label(mask[0])
bounding_boxes = ndimage.find_objects(labeled_array)

centers = []
for box in bounding_boxes:
    y_center = (box[0].start + box[0].stop - 1) / 2
    x_center = (box[1].start + box[1].stop - 1) / 2
    centers.append((x_center, y_center))

labels, n = ndimage.label(mask[0])
num_dark_spots = n
print("Number of sunspots: ", num_dark_spots)

plt.xticks([])
plt.yticks([])

plt.imshow(data_masked[0], cmap = "gray", origin = "lower")
plt.colorbar()

x_coord, y_coord = zip(*centers)
plt.scatter(x_coord, y_coord, c = "red", marker = "x")

plt.show()
