# Jon Zarate
# Shea A. Hess Webber
# Milo Buitrago-Casas
# Exploring the Unseen Sun
# Date Created: 06-21-2023
#
#

import fsi_functions as fsi


series = 'hmi.td_fsi_12h'
email = 'jjzarate215@berkeley.edu'
f_rec = '2011.02.01_00:00:00_TAI'      #year.month.day_time_TAI
l_rec = '2022.02.01_12:00:00_TAI'
fsi_directory = 'C:\\Users\\Jjzar\\OneDrive\\Documents\\ASSURE\\ASSURE 2023\\Exploring the Unseen Sun\\Far-SideImagingData\\2011-2022'

#hmi_downloader(series, email, f_rec, l_rec, fsi_directory)
results = fsi.extract_fsi_data(fsi_directory)
results2 = fsi.create_mask(results['image datum'], results['image mean pix val'])



#1) moving average for average pixel values (maybe 6)
#2) track sunspot to near-side (maybe use sunpy?, NOAA ar number(how many flares occured))
# use centroid to keep track of far side ar
#
#4) find average pixel values of only of the dark regions (convert 0s to nan, then use nanmean() )




import matplotlib.pyplot as plt
#to use year locator
import matplotlib.dates as mdates

## Added two new imports here
from matplotlib import ticker


# ## This line is useful if you want to ultimately plot more than one plot in the same figure
fig, axs = plt.subplots(1, 1, figsize=(16, 7))

axs.plot(results['image headers'], results['image mean pix val'], color = 'red') #note the new x-axis variable!
plt.xlabel('Observed Time')
plt.ylabel('Average Pixel Value')
plt.title('Average Phase Shift 2011-2022')

axs.tick_params(axis='x', rotation=55)
axs.xaxis.set_major_locator(mdates.YearLocator())

plt.show()

fig1, axs1 = plt.subplots(1, 1, figsize=(16, 7), layout='constrained')

axs1.plot(results['image headers'], results2['mask data mean'], color = 'blue') #note the new x-axis variable!
plt.xlabel('Observed Time')
plt.ylabel('Average Pixel Value of Dark Regions - without NaNs')
plt.title('Average Phase Shift 2011-2022')

axs1.tick_params(axis='x', rotation=55)
axs1.xaxis.set_major_locator(mdates.YearLocator())

plt.show()








# #improve on the future
# labeled_array, num_features = ndimage.label(bool_mask[0])
# bounding_boxes = ndimage.find_objects(labeled_array)

# centers = []
# for box in bounding_boxes:
#     y_center = (box[0].start + box[0].stop - 1) / 2
#     x_center = (box[1].start + box[1].stop - 1) / 2
#     centers.append((x_center, y_center))

# # labels, n = ndimage.label(mask[0])
# # num_dark_spots = n
# # print("Number of sunspots: ", num_dark_spots)
# print("Number of sunspots: ", dark_regions[0])

# plt.xticks([])
# plt.yticks([])

# plt.imshow(mask_data[0], cmap = "gray", origin = "lower")
# plt.colorbar()

# x_coord, y_coord = zip(*centers)
# plt.scatter(x_coord, y_coord, c = "red", marker = "x")

# plt.show()
