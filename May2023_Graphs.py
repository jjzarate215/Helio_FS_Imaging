# Jon Zarate
# Shea A. Hess Webber
# Milo Buitrago-Casas
# Exploring the Unseen Sun
# Date Created: 06-21-2023
#
#

# import sunpy
# from sunpy.net import Fido
# from sunpy.net import attrs as a


# jsoc_email = "jjzarate215@berkeley.edu"

# query = Fido.search(
#     a.Time('2023.05.01_00:00:00_TAI', '2023.05.31_12:00:00_TAI'),
#     a.jsoc.Series('hmi.td_fsi_12h'),
#     a.jsoc.Notify(jsoc_email)
# )

# print(query)
# directory = 'C:\\Users\\Jjzar\\OneDrive\\Documents\\ASSURE\\ASSURE 2023\\Exploring the Unseen Sun\\Far-SideImagingData\\May2023'
# download_fsi = Fido.fetch(query, path = directory)

#########################################################################
import os
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

fsi_directory = 'C:\\Users\\Jjzar\\OneDrive\\Documents\\ASSURE\\ASSURE 2023\\Exploring the Unseen Sun\\Far-SideImagingData\\May2023'
fsi_images = []
fsi_images_data =[]
fsi_headers = []

for fsi_file in os.listdir(fsi_directory):
    if os.path.isfile(os.path.join(fsi_directory, fsi_file)):
        fsi_images.append(fsi_file)

        hdu = fits.open(os.path.join(fsi_directory, fsi_file))
        image_data = hdu[0].data
        image_header = hdu[0].header['DATE-OBS']
        hdu.close()

        fsi_images_data.append(image_data)
        fsi_headers.append(image_header)


#print(fsi_images)
#print(len(fsi_images))

print(fsi_headers)
print(len(fsi_headers))

avg_may = []
for image_data in fsi_images_data:
    average_value = np.nanmean(image_data)

    avg_may.append(average_value)

#print(avg_may)
#print(len(avg_may))


# print(fsi_images[2])
# plt.imshow(fsi_images_data[2], cmap = 'gray')
# plt.show()

plt.scatter(fsi_headers, avg_may, color = 'red')
plt.xlabel('Observed Time')
plt.xticks(rotation = 'vertical')
plt.ylabel('Average Pixel Value')
plt.title('Untitled')
plt.show()
